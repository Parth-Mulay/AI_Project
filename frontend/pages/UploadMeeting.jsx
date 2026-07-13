import React, { useState, useEffect } from 'react';
import Input from '../components/Input';
import Button from '../components/Button';

export default function UploadMeeting({ onAddMeeting, onPageChange }) {
  const [formData, setFormData] = useState({
    title: '',
    datetime: '',
    duration: '30',
    category: 'Planning',
    participants: '',
    file: null
  });

  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [uploadStage, setUploadStage] = useState(0); // 0 to 5
  const [dragActive, setDragActive] = useState(false);
  const [successMeeting, setSuccessMeeting] = useState(null);

  const pipelineStages = [
    { label: 'Reading document...', icon: 'description' },
    { label: 'Extracting text...', icon: 'find_in_page' },
    { label: 'Analyzing meeting notes...', icon: 'psychology' },
    { label: 'Generating AI summary...', icon: 'summarize' },
    { label: 'Extracting action items...', icon: 'playlist_add_check' },
    { label: 'Syncing to workspace...', icon: 'sync' }
  ];

  // Pipeline simulation timers
  useEffect(() => {
    let interval = null;
    if (isSubmitting) {
      interval = setInterval(() => {
        setUploadStage((prev) => {
          if (prev >= pipelineStages.length - 1) {
            clearInterval(interval);
            handlePipelineComplete();
            return prev;
          }
          return prev + 1;
        });
      }, 1000);
    }
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [isSubmitting]);

  const handleInputChange = (field, value) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
    if (errors[field]) {
      setErrors((prev) => ({ ...prev, [field]: '' }));
    }
  };

  const handleFileChange = (file) => {
    if (!file) return;

    // Client-side secure validation: file size and extension checks
    const allowedExtensions = ['docx', 'pdf', 'txt', 'mp3', 'wav'];
    const extension = file.name.split('.').pop().toLowerCase();
    
    if (!allowedExtensions.includes(extension)) {
      setErrors((prev) => ({
        ...prev,
        file: `Invalid extension .${extension}. Permitted: ${allowedExtensions.join(', ')}`
      }));
      setFormData((prev) => ({ ...prev, file: null }));
      return;
    }

    // Size check: Docs (docx, pdf, txt) max 10MB, Audio (mp3, wav) max 100MB
    const isAudio = ['mp3', 'wav'].includes(extension);
    const maxSize = isAudio ? 100 * 1024 * 1024 : 10 * 1024 * 1024;

    if (file.size > maxSize) {
      const sizeLabel = isAudio ? '100MB' : '10MB';
      setErrors((prev) => ({
        ...prev,
        file: `File size exceeds the ${sizeLabel} limit for ${isAudio ? 'audio' : 'document'} files.`
      }));
      setFormData((prev) => ({ ...prev, file: null }));
      return;
    }

    setFormData((prev) => ({ ...prev, file }));
    setErrors((prev) => ({ ...prev, file: '' }));
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileChange(e.dataTransfer.files[0]);
    }
  };

  const validateForm = () => {
    const newErrors = {};

    if (!formData.title.trim()) {
      newErrors.title = 'Meeting Title is required';
    } else if (formData.title.length < 5) {
      newErrors.title = 'Title must be at least 5 characters long';
    }

    if (!formData.datetime) {
      newErrors.datetime = 'Meeting Date & Time is required';
    }

    const durationNum = parseInt(formData.duration, 10);
    if (!formData.duration || isNaN(durationNum) || durationNum <= 0) {
      newErrors.duration = 'Please provide a valid duration in minutes';
    }

    const participantsList = formData.participants
      .split(',')
      .map((p) => p.trim())
      .filter((p) => p !== '');
    if (!formData.participants.trim()) {
      newErrors.participants = 'Please specify participants';
    } else if (participantsList.length < 2) {
      newErrors.participants = 'Please specify at least 2 participants (comma separated)';
    }

    if (!formData.file) {
      newErrors.file = 'Please upload a meeting document or audio file';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!validateForm()) return;

    setIsSubmitting(true);
    setUploadStage(0);
  };

  const handlePipelineComplete = () => {
    // Generate mock AI summary meeting results
    const participantsArray = formData.participants
      .split(',')
      .map((p) => p.trim())
      .filter((p) => p !== '');

    const newMeeting = {
      id: String(Date.now()),
      title: formData.title,
      date: formData.datetime.split('T')[0],
      time: new Date(formData.datetime).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      duration: `${formData.duration} minutes`,
      participants: participantsArray,
      tags: [formData.category.toLowerCase()],
      status: 'Analyzed',
      summary: `## Executive Summary
All departments aligned key plans under the ${formData.category} agenda. Major agreements included a budget expansion.

## Key Discussion Points
- Detailed discussion of ${formData.title}.
- Focus on performance tracking.

## Risks
- Staffing schedules require alignment.`,
      actionItems: [
        { task: `Verify action items for ${formData.title}`, owner: participantsArray[0] || 'Priya', deadline: 'Jul 20', priority: 'High', status: 'Pending' },
        { task: 'Review pipeline output data', owner: participantsArray[1] || 'Rahul', deadline: 'Jul 25', priority: 'Medium', status: 'Pending' }
      ],
      decisions: [
        `Approved roadmap for ${formData.category}.`,
        'Decided on database layout optimizations.'
      ]
    };

    setSuccessMeeting(newMeeting);
    setIsSubmitting(false);
  };

  const handleAddSuccessMeeting = () => {
    if (successMeeting) {
      onAddMeeting(successMeeting);
      onPageChange('dashboard');
    }
  };

  return (
    <div className="view-panel">
      <div className="view-header">
        <h2>Upload Meeting Audio & Documents</h2>
        <p className="subtitle">
          Extract transcripts and AI insights dynamically from standard file extensions.
        </p>
      </div>

      <div className="upload-container">
        {/* SUCCESS STATE */}
        {successMeeting ? (
          <div className="success-preview-container" role="status" aria-live="polite">
            <div className="success-header-row">
              <span className="material-symbols-outlined" style={{ fontSize: '32px' }}>
                check_circle
              </span>
              <h3>Meeting Notes Processed Successfully!</h3>
            </div>
            
            <div className="success-preview-body">
              <p><strong>Title:</strong> {successMeeting.title}</p>
              <p><strong>Category:</strong> {formData.category}</p>
              <p><strong>Duration:</strong> {successMeeting.duration}</p>
              <p><strong>Participants:</strong> {successMeeting.participants.join(', ')}</p>
              <p style={{ marginTop: '12px', borderTop: '1px solid var(--color-border-glass)', paddingTop: '12px' }}>
                <strong>🤖 Summary Preview:</strong> We have extracted 2 Action Items and 2 Decisions from your meeting transcripts.
              </p>
            </div>

            <div style={{ display: 'flex', gap: '12px', marginTop: '8px' }}>
              <Button onClick={handleAddSuccessMeeting}>
                Add to Dashboard & View
              </Button>
              <Button variant="secondary" onClick={() => setSuccessMeeting(null)}>
                Upload Another File
              </Button>
            </div>
          </div>
        ) : isSubmitting ? (
          /* LOADING PIPELINE STATE */
          <div className="upload-log-container" role="status" aria-live="polite">
            <div className="file-details-card">
              <div className="file-info">
                <span className="material-symbols-outlined file-icon" style={{ fontSize: '28px' }}>
                  description
                </span>
                <div>
                  <h4>{formData.file?.name}</h4>
                  <span>{(formData.file?.size / (1024 * 1024)).toFixed(2)} MB</span>
                </div>
              </div>
              <span className="badge processing">Processing</span>
            </div>

            <div className="pipeline-loader">
              <h3 className="loader-header">AI Synthesis Pipeline</h3>
              <ul className="loader-stages">
                {pipelineStages.map((stage, idx) => {
                  let statusClass = 'pending';
                  let iconSymbol = 'circle';

                  if (idx < uploadStage) {
                    statusClass = 'done';
                    iconSymbol = 'check_circle';
                  } else if (idx === uploadStage) {
                    statusClass = 'active';
                    iconSymbol = 'sync';
                  }

                  return (
                    <li key={idx} className={`stage-item ${statusClass}`}>
                      <span className="stage-indicator">
                        <span className="material-symbols-outlined" style={{
                          color: statusClass === 'done' ? 'var(--color-accent-green)' : 
                                 statusClass === 'active' ? 'var(--color-accent-purple)' : 'var(--color-text-secondary)'
                        }}>
                          {iconSymbol}
                        </span>
                      </span>
                      <span>{stage.label}</span>
                    </li>
                  );
                })}
              </ul>
            </div>
          </div>
        ) : (
          /* ACTIVE FORM INPUT STATE */
          <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
            {/* Controlled inputs using custom components */}
            <Input
              label="Meeting Title"
              id="form-title"
              value={formData.title}
              onChange={(e) => handleInputChange('title', e.target.value)}
              placeholder="e.g. Engineering Sprint Planning"
              error={errors.title}
              required
            />

            <div className="form-row-grid">
              <Input
                label="Date & Time"
                id="form-datetime"
                type="datetime-local"
                value={formData.datetime}
                onChange={(e) => handleInputChange('datetime', e.target.value)}
                error={errors.datetime}
                required
              />

              <Input
                label="Duration (minutes)"
                id="form-duration"
                type="number"
                value={formData.duration}
                onChange={(e) => handleInputChange('duration', e.target.value)}
                placeholder="e.g. 30"
                error={errors.duration}
                required
              />
            </div>

            <div className="form-row-grid">
              <div className="input-group">
                <label htmlFor="form-category" className="input-label">
                  Category
                </label>
                <select
                  id="form-category"
                  value={formData.category}
                  onChange={(e) => handleInputChange('category', e.target.value)}
                  className="input-field"
                  style={{ cursor: 'pointer' }}
                >
                  <option value="Planning">Planning</option>
                  <option value="Marketing">Marketing</option>
                  <option value="Operations">Operations</option>
                  <option value="HR">HR</option>
                  <option value="Engineering">Engineering</option>
                </select>
              </div>

              <Input
                label="Participants (comma separated)"
                id="form-participants"
                value={formData.participants}
                onChange={(e) => handleInputChange('participants', e.target.value)}
                placeholder="e.g. Priya, Rahul, Amit"
                error={errors.participants}
                required
              />
            </div>

            {/* Drag & Drop File Zone */}
            <div className="input-group">
              <span className="input-label">Meeting Audio or Transcript File</span>
              <div
                className={`drag-drop-zone ${dragActive ? 'active-drag' : ''}`}
                onDragEnter={handleDrag}
                onDragOver={handleDrag}
                onDragLeave={handleDrag}
                onDrop={handleDrop}
                onClick={() => document.getElementById('file-selector')?.click()}
                role="button"
                tabIndex={0}
                aria-label="Upload File Dropzone. Drag files here or click to browse"
                onKeyDown={(e) => {
                  if (e.key === 'Enter' || e.key === ' ') {
                    document.getElementById('file-selector')?.click();
                  }
                }}
              >
                <span className="upload-cloud-icon">
                  <span className="material-symbols-outlined" style={{ fontSize: '48px', color: 'var(--color-accent-purple)' }}>
                    cloud_upload
                  </span>
                </span>
                <h3>Drag & Drop Meeting Files Here</h3>
                <p>or click to browse your local filesystem</p>
                <span className="formats-lbl">
                  Supported: .docx, .pdf, .txt, .mp3, .wav (Max sizes: Docs 10MB, Audio 100MB)
                </span>
                <input
                  id="file-selector"
                  type="file"
                  onChange={(e) => handleFileChange(e.target.files?.[0])}
                  style={{ display: 'none' }}
                  accept=".docx,.pdf,.txt,.mp3,.wav"
                />
              </div>

              {formData.file && (
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginTop: '10px', color: 'var(--color-accent-green)' }}>
                  <span className="material-symbols-outlined" style={{ fontSize: '18px' }}>
                    check_circle
                  </span>
                  <span>Attached: <strong>{formData.file.name}</strong> ({(formData.file.size / (1024 * 1024)).toFixed(2)} MB)</span>
                </div>
              )}

              {errors.file && (
                <span className="error-text" role="alert" style={{ marginTop: '8px' }}>
                  ⚠️ {errors.file}
                </span>
              )}
            </div>

            {/* Form actions */}
            <div style={{ display: 'flex', gap: '12px', marginTop: '10px' }}>
              <Button type="submit" variant="ai">
                Upload & Process with AI
              </Button>
              <Button variant="secondary" onClick={() => onPageChange('dashboard')}>
                Cancel
              </Button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
}
