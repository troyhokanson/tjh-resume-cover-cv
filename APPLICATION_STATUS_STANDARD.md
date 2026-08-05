# Troy Hokanson Application Status and Google Drive Filing Standard

Purpose: keep Troy Hokanson's application materials and application-status records controlled across Google Drive, Notion, GitHub, and generated documents.

## Source of truth

Troy's application document source of truth is:

- GitHub repo: `troyhokanson/tjh-resume-cover-cv`
- Notion hub: `Investigator Command Center`
- Google Drive active applications folder: `09_Applications/Troy Applications`

The active Google Drive applications folder URL is:

- `https://drive.google.com/drive/folders/1vUi8B5AnJN9pkBOB69a9X5O1DvrQWSE1`

## Candidate-specific Drive convention

Troy and Melissa use the same folder-name convention, but their application roots are separate:

- Troy application folders live under `09_Applications/Troy Applications`;
- each folder begins with the application date in `YYYY-MM-DD` format;
- each application has its own folder;
- generated resumes, cover letters, CVs, PDFs, DOCX files, job descriptions, validation reports, and relevant communications belong in that dated folder;
- legacy materials live in legacy application folders, not mixed with the current active workflow.

Examples:

- `2026-07-19 OpenAI Child Safety`
- `2026-07-17 Metro State Adjunct Application`
- `2026-07-16_Flock_Cust_Serv_Mgr`

## Candidate boundary rule

The Drive folder-name convention is shared. The candidate roots and workflows are separate.

- Troy document workflow: `troyhokanson/tjh-resume-cover-cv`
- Melissa document workflow: `troy-hokanson/auditorsearchbot`
- Troy status tracking belongs in the Investigator Command Center / Troy application records.
- Melissa status tracking belongs in `Melissa — Application Status Tracker`.

Do not process Melissa resumes, cover letters, CVs, or application statuses through Troy's document standards. Do not process Troy investigator/public-safety applications through Melissa's healthcare/auditor standards.

## Automatic status trigger

If the user pastes or uploads a Troy job-search communication, treat it as an application-status event, not just a chat message.

Trigger examples:

- application confirmation;
- recruiter outreach;
- interview request;
- scheduling message;
- rejection or no-thank-you notice;
- offer;
- withdrawal;
- follow-up request.

## Required action

For each triggered communication, the assistant must:

1. Identify the likely company, role, communication type, and status.
2. Search for an existing matching Troy application record in Notion, the Career Evidence Master, or the dated Drive folders when available.
3. Update the existing record when company and role match.
4. Create a new record when no matching record exists and the source system allows it.
5. Record the status, date, next action, recruiter/contact, and source link when available.
6. Link or name the matching dated Google Drive application folder.
7. Confirm the update back to the user in chat.

## Required user-facing confirmation

After any Notion, GitHub, Google Drive, or spreadsheet update, the assistant must confirm in chat:

- what system was updated;
- what page, database, repo, spreadsheet, or Drive folder was changed;
- what status, folder link, rule, or field changed;
- what remains open, if anything.

The user should not have to ask whether an update was completed.
