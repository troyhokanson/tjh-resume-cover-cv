# Troy Hokanson Contact Standard

**Permanent. Applies to every resume, cover letter, CV, recruiter packet, professional bio, one-pager, PDF, DOCX, and application document bearing Troy Hokanson's name.**

## Canonical values

- Email: `TroyHokanson@iCloud.com`
- LinkedIn display: `linkedin.com/in/troyhokanson`
- Portfolio display: `TroyHokanson.com`
- Portfolio target: `https://TroyHokanson.com`

Do not use `Troy.Hokanson@pm.me` or the retired GitHub Pages portfolio address in application documents.

## Locked page-one order

The single-line contact row must appear in this order:

1. Location
2. Phone, when supplied
3. Email
4. LinkedIn
5. `TroyHokanson.com`

The portfolio is always the far-right item immediately after LinkedIn. Its visible text must be `TroyHokanson.com`, not `Investigative Portfolio`.

## Build rule

Templates load contact values from `config.py`. Private values remain in local environment variables or repository secrets. Public canonical values may use the safe defaults defined in `config.py`.

```bash
TROY_EMAIL=TroyHokanson@iCloud.com
TROY_LINKEDIN=linkedin.com/in/troyhokanson
TROY_PORTFOLIO=https://TroyHokanson.com
```

## Mandatory delivery gate

Every final resume and cover letter pair must be checked together before delivery:

```bash
python delivery_gate.py RESUME.pdf COVER_LETTER.pdf --profile PROFILE
```

Use `--icac` only for accurately documented ICAC/child-safety materials. The command must exit `0`. It hard-fails if the portfolio is missing, appears before LinkedIn, or either file fails `anti_ai_scan.py`.

## AI build rule

An AI-assisted build must use these defaults automatically. Do not ask Troy to restate the portfolio placement or remind the system to run both scans. If a generated draft conflicts with this file, this file controls.
