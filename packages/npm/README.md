# disposable-email-domain

[![npm](https://img.shields.io/npm/v/disposable-email-domain.svg)](https://www.npmjs.com/package/disposable-email-domain)
[![downloads](https://img.shields.io/npm/dm/disposable-email-domain.svg)](https://www.npmjs.com/package/disposable-email-domain)
[![license](https://img.shields.io/npm/l/disposable-email-domain.svg)](https://github.com/mehrtat/disposable-email-domain/blob/main/LICENSE)

A large, **auto-updated** list of disposable / temporary / throwaway email domains (mailinator, 10minutemail, guerrillamail, …), with a tiny zero-dependency `isDisposable()` helper.

- **160,000+ domains**, aggregated from 6 well-maintained public blocklists, deduped and normalized (lowercased, IDNA/punycode).
- **refreshed weekly** by a GitHub Action — a new version is published only when the set actually changes.
- **Zero dependencies.** Ships the raw list too, so you can use it however you like.

## Install

```bash
npm install disposable-email-domain
```

## Usage

```ts
import { isDisposable, domains } from "disposable-email-domain";

isDisposable("someone@mailinator.com"); // true
isDisposable("someone@gmail.com");      // false
isDisposable("mailinator.com");         // true (bare domain also works)

domains.length; // 160000+  — the full array if you want it
```

CommonJS:

```js
const { isDisposable } = require("disposable-email-domain");
```

`isDisposable(input)` accepts a full email (`user@domain`) or a bare domain, is case-insensitive, and returns `boolean`.

## Why

Blocking disposable-email signups cuts fraud, fake accounts, and junk. Hand-maintaining such a list is a losing battle — this package keeps it fresh for you automatically.

## Data sources

Aggregated + deduped from: `disposable/disposable-email-domains`, `ivolo/disposable-email-domains`, `FGRibreau/mailchecker`, `wesbos/burner-email-providers`, `disposable-email-domains/disposable-email-domains`, `7c/fakefilter`. Credit to their maintainers.

## Also available for

Go — `go get github.com/mehrtat/disposable-email-domain` · .NET — `dotnet add package DisposableEmailDomain`

Source, issues, and how to contribute a source: **https://github.com/mehrtat/disposable-email-domain**

## License

MIT © Mehrdad TAT
