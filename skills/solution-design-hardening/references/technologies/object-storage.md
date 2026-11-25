# S3-compatible object storage / MinIO

Related baseline problems: SDP-092, SDP-094, SDP-095, SDP-097, SDP-099, SDP-124, SDP-159.

## Detection
Inspect object upload versus metadata commits, presigned URLs, cleanup criteria, version checks and lifecycle retention.

## Implementation
Use unique staging keys, verify object integrity, finalize metadata with conditional state transitions and reconcile abandoned uploads. Authorize object access by tenant; use short-lived URLs and conditional writes/deletes where supported.

## Pitfalls / counterexamples
ETag is not universally a content MD5. Object-store consistency and conditional operations vary by provider/version; do not assume a database transaction includes object storage.

## Verification
Interrupt upload and finalization independently, race cleanup with finalization and verify no valid reference loses its object; validate replay retention.

## Upstream reference
[Official documentation](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html). Confirm installed versions and provider capabilities before selecting APIs. This is guidance, not a tested integration.
