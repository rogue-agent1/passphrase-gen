# passphrase

Generate secure passphrases, passwords, and PINs. Zero dependencies.

## Commands

```bash
passphrase phrase -w 5 -n 3 --cap    # 5-word passphrases, capitalized
passphrase password -l 20 -n 3       # 20-char passwords
passphrase pin -l 8                  # 8-digit PIN
passphrase check "MyPassword123"     # Analyze strength
```

## Features

- Passphrase: 200-word built-in dictionary, custom separator
- Password: letters + digits + symbols, configurable length
- Strength: entropy calculation with visual rating
- Check: analyze existing passwords

## Requirements

- Python 3.6+ (stdlib only)
