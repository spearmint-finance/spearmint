# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in Spearmint, please report it responsibly.

**Do NOT open a public GitHub issue for security vulnerabilities.**

Instead, please email **security@spearmint.finance** with:

1. A description of the vulnerability
2. Steps to reproduce
3. Potential impact
4. Suggested fix (if you have one)

We will acknowledge your report within 48 hours and aim to provide a fix within 7 days for critical issues.

## Supported Versions

| Version | Supported |
|---------|-----------|
| Latest  | Yes       |

## Security Considerations

Spearmint is a self-hosted application that handles personal financial data. Key security notes:

- **Authentication:** Currently in development (#141). Until shipped, do not expose Spearmint to untrusted networks.
- **Data storage:** All data stays on your hardware. No telemetry or external data transmission.
- **Database:** SQLite (dev) or PostgreSQL (prod). Ensure your database is not exposed to the network.
- **Docker:** Default PostgreSQL credentials should be changed via environment variables before any non-local deployment.

## Best Practices for Self-Hosting

1. Run behind a reverse proxy (nginx, Caddy) with HTTPS
2. Change default database credentials via environment variables
3. Keep your instance updated to the latest version
4. Restrict network access to trusted users until authentication is implemented
5. Back up your database regularly
