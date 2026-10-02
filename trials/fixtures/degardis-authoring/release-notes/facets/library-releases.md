---
title: Libraries and SDKs
category: Product
description: Releases consumed by other developers' code, such as packages, SDKs, and client libraries.
---

Readers of library release notes are developers deciding whether and how to
upgrade a dependency. Under semantic versioning, a major version signals
incompatible changes, a minor version adds compatible features, and a patch
fixes bugs, so a version bump that disagrees with the changes misleads readers
who upgrade by version range.

For libraries, count a change as breaking only when it removes or renames a
public API; a change in behavior behind an unchanged signature belongs under
Improvements.

Developers judge a changed API by its old and new call, so an entry for one is
most useful with both shown side by side, in the library's own language.

Before delivering notes for a library release with breaking changes, add an
Upgrade section with numbered steps a developer can follow, one for each
breaking change; notes without one are not finished.
