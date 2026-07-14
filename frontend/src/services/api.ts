export interface MeetingSummary {
  id: string;
  title: string;
  created_at: string;
  participants: string[];
  message_count: number;
}

/** Fetch list of meetings */
export const fetchMeetings = async (): Promise<MeetingSummary[]> => {
  const resp = await fetch(`${import.meta.env.VITE_API_URL}/meetings`);
  if (!resp.ok) throw new Error('Failed to load meetings');
  return resp.json();
};

/** Fetch a single meeting detail */
export const fetchMeeting = async (id: string) => {
  const resp = await fetch(`${import.meta.env.VITE_API_URL}/meetings/${id}`);
  if (!resp.ok) throw new Error('Failed to load meeting');
  return resp.json();
};

/** Upload a document */
export const uploadDocument = async (file: File) => {
  const form = new FormData();
  form.append('file', file);
  const resp = await fetch(`${import.meta.env.VITE_API_URL}/upload`, {
    method: 'POST',
    body: form,
  });
  if (!resp.ok) throw new Error('Upload failed');
  return resp.json();
};

/** Export meeting as markdown */
export const exportMeeting = async (id: string) => {
  const resp = await fetch(`${import.meta.env.VITE_API_URL}/meetings/${id}/export`);
  if (!resp.ok) throw new Error('Export failed');
  return resp.blob();
};
