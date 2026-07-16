# Debugging with Breakpoints

## Approach
1. Reproduce the issue with the smallest available test or script.
2. Pause execution at the failing boundary and inspect the request, state, and imported modules.
3. Confirm whether the failure is caused by import resolution, route registration, or runtime dependency availability.
4. Apply the smallest root-cause fix and re-run the test.

## Key Findings
- The import issue was rooted in inconsistent import styles between modules invoked by pytest and modules invoked by the server.
- The upload route issue was caused by route interception and not by the upload handler body itself.
- The NLP failure was caused by optional dependency availability rather than incorrect business logic.
