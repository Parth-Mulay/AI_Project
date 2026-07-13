# Research References – AI Meeting Notes Manager

## Executive Summary

This document catalogs the key resources, frameworks, and learning materials consulted during the research and development of the AI Meeting Notes Manager. All references are verified and publicly available. Resources are organized by domain to support continued learning, future product choices, and engineering alignment.

---

## 1. Product Management & Strategy

- **Resource:** *Inspired: How to Create Products Customers Love* by Marty Cagan (Silicon Valley Product Group)
  - **Why It Was Consulted:** Consulted to align our product discovery workflow with industry standards, focusing on identifying user value and viability risks early.
  - **How It Influenced This Project:** Guided the decision to prioritize problem validation and customer pain points before writing code. This led to focusing on structured outcome extraction as the core product feature.
- **Resource:** *Empowered: Ordinary People, Extraordinary Products* by Marty Cagan (Silicon Valley Product Group)
  - **Why It Was Consulted:** Consulted to understand team alignment, ownership structure, and empowerment in cross-functional software environments.
  - **How It Influenced This Project:** Influenced the decision to design a tool-agnostic export format (Markdown) that empowers different teams (designers, PMs, engineers) to own and integrate their meeting outcomes without proprietary software restrictions.
- **Resource:** Silicon Valley Product Group Resources (svpg.com)
  - **Why It Was Consulted:** Consulted for articles regarding product-market fit, prototyping, and discovery methods.
  - **How It Influenced This Project:** Helped clarify the distinction between low-fidelity prototypes (mockups) and high-fidelity code prototypes (our current CLI implementation) to validate solution viability.
- **Resource:** Product School Learning Hub (productschool.com)
  - **Why It Was Consulted:** Consulted for training resources, template designs, and industry product manager workflows.
  - **How It Influenced This Project:** Helped refine the Emma Park (Product Manager) user persona, mapping the specific post-meeting documentation overhead and context-switching challenges PMs experience.

---

## 2. UX Research & Design

- **Resource:** Nielsen Norman Group (nngroup.com)
  - **Why It Was Consulted:** Consulted to apply verified usability heuristics and understand cognitive load theory.
  - **How It Influenced This Project:** Guided the CLI design to show real-time feedback (such as status updates during processing) and prioritized a simple dialogue capture loop to minimize the note-taker's cognitive load.
- **Resource:** *The Design of Everyday Things* by Don Norman
  - **Why It Was Consulted:** Consulted to evaluate fundamental design concepts (affordances, signifiers, feedback, and constraints) in user interfaces.
  - **How It Influenced This Project:** Influenced the console formatting, ensuring that output headers, separators, and Unicode icons act as visual signifiers to organize structured notes for the user.
- **Resource:** UX Collective (uxdesign.cc)
  - **Why It Was Consulted:** Consulted for case studies and articles on digital product design and text-heavy interface layouts.
  - **How It Influenced This Project:** Helped establish layout formatting rules for our exported Markdown reports, ensuring they are clean, readable, and scan-friendly.

---

## 3. Lean Startup & Design Thinking

- **Resource:** *The Lean Startup* by Eric Ries
  - **Why It Was Consulted:** Consulted to apply the build-measure-learn feedback loop and MVP scope constraints.
  - **How It Influenced This Project:** Guided our lean scope, directing the implementation of a rule-based parser in the prototype rather than integrating expensive, complex API calls from day one.
- **Resource:** Lean Startup Methodology Resources (leanstartup.co)
  - **Why It Was Consulted:** Consulted for guidelines on validating core hypotheses with minimal resource allocation.
  - **How It Influenced This Project:** Reinforced the decision to run the prototype fully locally using Python's standard library to validate customer problem-solution fit.
- **Resource:** IDEO Design Thinking Resources (designthinking.ideo.com)
  - **Why It Was Consulted:** Consulted for frameworks on human-centered design (empathize, define, ideate, prototype, test).
  - **How It Influenced This Project:** Guided our user discovery phase, leading to the creation of three distinct user personas (Emma, Carlos, Nina) mapping unique goals, behaviors, and pain points.

---

## 4. AI Product Design & LLM Considerations

- **Resource:** OpenAI API Documentation (platform.openai.com/docs)
  - **Why It Was Consulted:** Consulted to study API schemas, prompt engineering structures, and limits of generative models.
  - **How It Influenced This Project:** Highlighted potential latency, API uptime dependencies, and hallucination risks, confirming the choice to use deterministic, rule-based keywords for our initial prototype.
- **Resource:** Anthropic Documentation (docs.anthropic.com)
  - **Why It Was Consulted:** Consulted to study context-window capabilities and predictable AI output structures.
  - **How It Influenced This Project:** Informed the modular service design, ensuring our extraction layer is isolated so an API client can be integrated in later phases without rewriting the core application.
- **Resource:** Google AI Documentation (ai.google/research)
  - **Why It Was Consulted:** Consulted for research articles concerning natural language processing, regex parser efficiency, and heuristic-based text extraction.
  - **How It Influenced This Project:** Guided the sentence-extraction heuristics used to compile meeting summaries by prioritizing sentences containing identified decisions and action items.

---

## 5. Software Engineering & Architecture

- **Resource:** Python Official Documentation (docs.python.org/3)
  - **Why It Was Consulted:** Consulted for standard library documentation, specifically text-processing (regex) and file management (pathlib) modules.
  - **How It Influenced This Project:** Enabled building the entire application using Python's standard library, ensuring zero-dependency execution and simple deployment.
- **Resource:** PEP 8 – Style Guide for Python Code (peps.python.org/pep-0008)
  - **Why It Was Consulted:** Consulted to ensure clean, readable, and standardized code formatting.
  - **How It Influenced This Project:** Guided class structures, naming conventions, docstring patterns, and type hints across all Python modules.
- **Resource:** Real Python (realpython.com)
  - **Why It Was Consulted:** Consulted for implementations of object-oriented design patterns (such as the Service layer pattern) and pytest configurations.
  - **How It Influenced This Project:** Influenced the creation of our modular directories, separating models (Meeting), services (Detection, Summarization, Export), and utilities (Formatter).
- **Resource:** Martin Fowler's Software Architecture Articles (martinfowler.com)
  - **Why It Was Consulted:** Consulted for design pattern references, specifically the Service Layer pattern and separation of concerns.
  - **How It Influenced This Project:** Helped isolate the parsing logic (`DetectionService`) from the file writer logic (`ExportService`), making each component independently testable.
- **Resource:** *Clean Architecture: A Craftsman's Guide to Software Structure and Design* by Robert C. Martin
  - **Why It Was Consulted:** Consulted to design a codebase with high maintainability and low coupling.
  - **How It Influenced This Project:** Informed the architectural boundary lines, ensuring that data models are decoupled from I/O presentation layers.

---

## 6. Prototype Validation

The working prototype implements and validates the architectural and software engineering guidelines documented in our references:
- **Clean Architecture Implementation:** The codebase maintains a strict separation of concerns. The `Meeting` model is independent of the CLI formatter and file export services, ensuring high maintainability.
- **PEP 8 Compliance:** All modules are formatted with standard Python conventions, featuring explicit type hints and detailed docstrings, ensuring technical reviewer readiness.
- **Standard Library Dependability:** By building the prototype using only standard Python components (like `re` and `pathlib`), we confirm the application's offline reliability and ease of local execution.

---

## 7. Conclusion

This research foundation supports the AI Meeting Notes Manager by grounding our product and technical choices in validated industry frameworks. Every design pattern, user segment, and architectural choice in the working prototype directly traces back to these verified resources.

---

**Document Status:** Refinement Completed  
**Date:** 2026-07-10  
**Version:** 1.1
