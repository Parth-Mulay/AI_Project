# src/nlp/pipeline.py
"""Advanced NLP Pipeline for AI Meeting Notes Manager.

Integrates spaCy, NLTK, and dateparser to dynamically extract meeting insights
(summary, action items, decisions, risks, deadlines, recommendations, statistics, and metadata)
completely offline without any hardcoded demo fallbacks.
"""

import re
import datetime
from typing import List, Dict, Any, Tuple
import dateparser
from .spacy_loader import get_nlp
from .text_cleaner import TextCleaner
from .sentence_segmenter import SentenceSegmenter

class MeetingNlpPipeline:
    """Orchestrates the offline NLP analysis of meeting documents."""

    def __init__(self):
        self.nlp = get_nlp()
        self.cleaner = TextCleaner()
        self.segmenter = SentenceSegmenter()

    def process(self, document_text: str, debug_mode: bool = False) -> Dict[str, Any]:
        """Process the raw document text and return structured meeting intelligence.

        Ensures document_text is the single source of truth.
        """
        # Step 1: Cleaning
        cleaned_text = self.cleaner.clean(document_text)

        # Step 2: Sentence Segmentation (Speaker-attributed)
        attributed_sentences = self.segmenter.segment(cleaned_text)

        # Preprocess sentences with spaCy Doc objects
        processed_sentences: List[Tuple[str, str, Any]] = []
        for speaker, sent in attributed_sentences:
            doc = self.nlp(sent)
            processed_sentences.append((speaker, sent, doc))

        # Character/Paragraph metrics
        char_count = len(document_text)
        paragraphs = [p.strip() for p in document_text.split('\n') if p.strip()]
        paragraph_count = len(paragraphs)

        # Step 3: Extract Metadata
        title, date, participants, departments, organizations, speakers, agenda = self._extract_metadata(
            document_text, processed_sentences
        )

        # Step 4: Extract Action Items
        action_items = self._extract_action_items(processed_sentences, participants)

        # Step 5: Extract Decisions
        decisions = self._extract_decisions(processed_sentences)

        # Step 6: Extract Risks
        risks = self._extract_risks(processed_sentences)

        # Step 7: Extract Deadlines list
        deadlines = self._extract_deadlines(processed_sentences)

        # Step 8: Generate Summary & Recommendations
        summary, recommendations = self._generate_summary_and_recommendations(
            processed_sentences, action_items, decisions, risks, title, date, participants
        )

        # Step 9: Compute Statistics
        statistics = {
            "total_messages": len(attributed_sentences),
            "paragraph_count": paragraph_count,
            "sentence_count": len(attributed_sentences),
            "extracted_text_length": char_count,
            "action_items_count": len(action_items),
            "decision_count": len(decisions),
            "risk_count": len(risks),
            "deadline_count": len(deadlines),
        }

        result = {
            "title": title,
            "date": date,
            "participants": participants,
            "departments": departments,
            "organizations": organizations,
            "speakers": speakers,
            "agenda": agenda,
            "summary": summary,
            "action_items": action_items,
            "decisions": decisions,
            "risks": risks,
            "deadlines": deadlines,
            "recommendations": recommendations,
            "statistics": statistics,
            "timeline": [{"speaker": s, "content": text} for s, text, _ in processed_sentences]
        }

        if debug_mode:
            self._print_developer_debug(result, document_text)

        return result

    def _extract_metadata(self, raw_text: str, processed_sentences: List[Tuple[str, str, Any]]) -> Tuple[str, datetime.date, List[str], List[str], List[str], List[str], str]:
        """Extract meeting metadata from raw text and attributed sentences."""
        title = "Untitled Meeting"
        meeting_date = datetime.date.today()
        participants = []
        departments = []
        organizations = []
        speakers = []
        agenda = ""

        # Extract Title
        lines = [line.strip() for line in raw_text.split('\n') if line.strip()]
        for line in lines[:5]:
            # Look for headers or explicit tags
            match = re.match(r'(?i)^(?:meeting\s+minutes|meeting\s+title|subject|meeting)\s*:\s*(.*)', line)
            if match:
                title = match.group(1).strip()
                break
        if title == "Untitled Meeting" and lines:
            # Fall back to the first line if short enough
            first_line = lines[0]
            if len(first_line) < 80:
                title = first_line.rstrip('#').strip()

        # Extract Date & Date strings
        date_pattern = re.compile(
            r'\b(?:\d{4}[-/]\d{1,2}[-/]\d{1,2}|\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{1,2},?\s+\d{4})\b',
            re.IGNORECASE
        )
        found_date = None
        for line in lines[:10]:
            match = date_pattern.search(line)
            if match:
                parsed_dt = dateparser.parse(match.group(0))
                if parsed_dt:
                    found_date = parsed_dt.date()
                    break
        if found_date:
            meeting_date = found_date

        # Extract departments & organizations using spaCy NER
        for _, _, doc in processed_sentences:
            for ent in doc.ents:
                if ent.label_ == "ORG":
                    org_name = ent.text.strip()
                    # Filter out common false positives
                    if org_name.lower() not in ["zoom", "teams", "slack", "http", "https"]:
                        if org_name not in organizations:
                            organizations.append(org_name)
                            # Heuristic for departments (ending in Dept, Department, Team)
                            if re.search(r'(?i)\b(?:dept|department|team|division)\b', org_name):
                                if org_name not in departments:
                                    departments.append(org_name)

        # Extract speaker names
        for speaker, _, _ in processed_sentences:
            if speaker != "Unknown" and speaker not in speakers:
                speakers.append(speaker)

        # Parse explicit participants lists or use extracted speakers
        for line in lines:
            match = re.match(r'(?i)^(?:participants|attendees|present)\s*:\s*(.*)', line)
            if match:
                names = [n.strip() for n in re.split(r'[,;]', match.group(1)) if n.strip()]
                for name in names:
                    if name not in participants:
                        participants.append(name)
        
        # Merge speakers into participants if participants is empty
        if not participants:
            participants = list(speakers)
        if not participants:
            participants = ["Unknown Participant"]

        # Extract Agenda
        agenda_lines = []
        capture = False
        for line in lines:
            if re.match(r'(?i)^(?:agenda|topics\s+to\s+discuss)\s*:', line):
                capture = True
                content = re.sub(r'(?i)^(?:agenda|topics\s+to\s+discuss)\s*:\s*', '', line).strip()
                if content:
                    agenda_lines.append(content)
                continue
            if capture:
                # Stop if another major heading starts
                if re.match(r'(?i)^(?:summary|action\s+items|decisions|risks)\b', line) or (line.startswith('#') and not line.startswith('###')):
                    break
                agenda_lines.append(line)
        if agenda_lines:
            agenda = "\n".join(agenda_lines).strip()

        return title, meeting_date, participants, departments, organizations, speakers, agenda

    def _extract_action_items(self, processed_sentences: List[Tuple[str, str, Any]], participants: List[str]) -> List[Dict[str, Any]]:
        """Extract action items with owner, task, deadline, priority, confidence."""
        action_items = []
        action_keywords = ["will", "must", "should", "need to", "needs to", "has to", "have to", "responsible for", "action item", "task", "follow-up"]

        for speaker, raw_sent, doc in processed_sentences:
            sent_lower = raw_sent.lower()
            # Must match at least one action keyword or pattern
            if any(kw in sent_lower for kw in action_keywords) or "assign" in sent_lower:
                # Extract Owner
                owner = "Unassigned"
                # Check for explicit assign pattern (e.g. "assign to Priya", "assigned to Amit")
                assign_match = re.search(r'(?i)assign(?:ed)?\s+to\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)', raw_sent)
                if assign_match:
                    owner = assign_match.group(1).strip()
                else:
                    # Check if the speaker is saying "I will..."
                    if re.search(r'(?i)\bi\s+(?:will|must|should|need\s+to|have\s+to)\b', raw_sent) and speaker != "Unknown":
                        owner = speaker
                    else:
                        # Scan for PERSON entities or names from participants list in the sentence
                        for ent in doc.ents:
                            if ent.label_ == "PERSON" and ent.text in participants:
                                owner = ent.text
                                break
                        if owner == "Unassigned":
                            for part in participants:
                                if part.lower() in sent_lower:
                                    owner = part
                                    break

                # Extract Deadline
                deadline = ""
                deadline_match = re.search(r'(?i)(?:by|before|due|deadline)\s+([A-Za-z0-9\s\-]{2,25}?)(?:\.|$|,|\s+and)', raw_sent)
                if deadline_match:
                    deadline_str = deadline_match.group(1).strip()
                    parsed_dt = dateparser.parse(deadline_str)
                    if parsed_dt:
                        deadline = parsed_dt.strftime("%Y-%m-%d")
                    else:
                        deadline = deadline_str
                else:
                    # Look for temporal words
                    if "tomorrow" in sent_lower:
                        deadline = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
                    elif "next week" in sent_lower:
                        deadline = "Next week"
                    elif "friday" in sent_lower:
                        deadline = "Friday"
                    elif "monday" in sent_lower:
                        deadline = "Monday"
                    elif "end of month" in sent_lower:
                        deadline = "End of Month"

                # Extract Priority
                priority = "Medium"
                if any(kw in sent_lower for kw in ["urgent", "critical", "immediately", "asap", "must"]):
                    priority = "High"
                elif any(kw in sent_lower for kw in ["low priority", "later", "whenever", "maybe"]):
                    priority = "Low"

                # Confidence Score Heuristic
                confidence = 0.5
                if owner != "Unassigned":
                    confidence += 0.2
                if deadline:
                    confidence += 0.15
                if any(kw in sent_lower for kw in ["will", "must", "action item"]):
                    confidence += 0.15
                confidence = min(confidence, 1.0)

                action_items.append({
                    "task": raw_sent,
                    "owner": owner,
                    "deadline": deadline or "Pending",
                    "priority": priority,
                    "original_sentence": raw_sent,
                    "confidence": round(confidence, 2)
                })

        return action_items

    def _extract_decisions(self, processed_sentences: List[Tuple[str, str, Any]]) -> List[Dict[str, Any]]:
        """Extract decisions with context, speaker, confidence."""
        decisions = []
        decision_keywords = ["approved", "agreed", "decided", "accepted", "confirmed", "resolved", "concluded"]

        for speaker, raw_sent, doc in processed_sentences:
            sent_lower = raw_sent.lower()
            if any(kw in sent_lower for kw in decision_keywords):
                # Confidence Score Heuristic
                confidence = 0.6
                if speaker != "Unknown":
                    confidence += 0.2
                if any(kw in sent_lower for kw in ["decided", "agreed"]):
                    confidence += 0.2
                confidence = min(confidence, 1.0)

                decisions.append({
                    "decision": raw_sent,
                    "speaker": speaker,
                    "context": raw_sent[:80] + ("..." if len(raw_sent) > 80 else ""),
                    "confidence": round(confidence, 2)
                })

        return decisions

    def _extract_risks(self, processed_sentences: List[Tuple[str, str, Any]]) -> List[Dict[str, Any]]:
        """Extract risks/blockers, filtering out simple "should" sentences."""
        risks = []
        risk_keywords = ["risk", "issue", "challenge", "delay", "concern", "dependency", "impact", "blocker", "problem", "bottleneck"]

        for speaker, raw_sent, doc in processed_sentences:
            sent_lower = raw_sent.lower()
            # Must explicitly match risk keywords, not just any modal
            if any(kw in sent_lower for kw in risk_keywords):
                # Avoid simple suggestions / options
                if "suggest" in sent_lower or "should we" in sent_lower:
                    continue

                confidence = 0.7
                if "blocker" in sent_lower or "risk" in sent_lower:
                    confidence = 0.9

                risks.append({
                    "description": raw_sent,
                    "speaker": speaker,
                    "confidence": round(confidence, 2)
                })

        return risks

    def _extract_deadlines(self, processed_sentences: List[Tuple[str, str, Any]]) -> List[str]:
        """Extract deadline sentences."""
        deadlines_list = []
        deadline_keywords = ["deadline", "due", "by tomorrow", "by friday", "by monday", "timeline", "target date"]

        for _, raw_sent, _ in processed_sentences:
            sent_lower = raw_sent.lower()
            if any(kw in sent_lower for kw in deadline_keywords):
                deadlines_list.append(raw_sent)

        return deadlines_list

    def _generate_summary_and_recommendations(
        self,
        processed_sentences: List[Tuple[str, str, Any]],
        action_items: List[Dict[str, Any]],
        decisions: List[Dict[str, Any]],
        risks: List[Dict[str, Any]],
        title: str,
        date: Any,
        participants: List[str]
    ) -> Tuple[str, List[str]]:
        """Generate a concise summary and action recommendations offline."""
        # 1. Generate Executive Summary
        # Extract the first few sentences as an overview, plus decisions and risks.
        intro_sentences = [text for _, text, _ in processed_sentences[:3]]
        overview = " ".join(intro_sentences)

        summary_parts = []
        summary_parts.append(f"## Executive Summary\nThe meeting '{title}' was held on {date}. Participants included: {', '.join(participants)}.\n\n{overview}\n")

        if decisions:
            summary_parts.append("## Key Decisions")
            for d in decisions:
                summary_parts.append(f"- {d['decision']}")
            summary_parts.append("")

        if action_items:
            summary_parts.append("## Action Items Checklist")
            for a in action_items:
                deadline_str = f" (Due: {a['deadline']})" if a['deadline'] != "Pending" else ""
                summary_parts.append(f"- [ ] **{a['owner']}**: {a['task']}{deadline_str}")
            summary_parts.append("")

        if risks:
            summary_parts.append("## Risks & Blockers")
            for r in risks:
                summary_parts.append(f"- {r['description']}")
            summary_parts.append("")

        summary_text = "\n".join(summary_parts).strip()

        # 2. Recommendations Heuristic
        recommendations = []
        if len(action_items) > 5:
            recommendations.append("High volume of action items detected. Consider scheduling a progress check-in.")
        if risks:
            recommendations.append("Active risks or blockers are present. Prioritize risk mitigation in next week's sync.")
        if not decisions:
            recommendations.append("No final decisions were recorded. Ensure key points are approved in the next meeting.")
        if not recommendations:
            recommendations.append("No immediate organizational recommendations. Team alignment looks solid.")

        return summary_text, recommendations

    def _print_developer_debug(self, data: Dict[str, Any], raw_text: str) -> None:
        """Print detailed developer debug mode logs."""
        print("\n" + "="*50)
        print("         DEVELOPER DEBUG LOG MODE")
        print("="*50)
        print(f" Loaded File           : [Document Upload]")
        print(f" Detected Title        : {data['title']}")
        print(f" Detected Date         : {data['date']}")
        print(f" Detected Participants : {', '.join(data['participants'])}")
        print(f" Paragraph Count       : {data['statistics']['paragraph_count']}")
        print(f" Sentence Count        : {data['statistics']['sentence_count']}")
        print(f" Extracted Text Length : {data['statistics']['extracted_text_length']} chars")
        print(f" Action Items Count    : {data['statistics']['action_items_count']}")
        print(f" Decision Count        : {data['statistics']['decision_count']}")
        print(f" Risk Count            : {data['statistics']['risk_count']}")
        print(f" Deadline Count        : {data['statistics']['deadline_count']}")
        print(f" Departments Extracted : {', '.join(data['departments'])}")
        print(f" Organizations Ext.    : {', '.join(data['organizations'])}")
        print("="*50 + "\n")
