# Code examples — 50 runnable teaching programs

Fresh examples written for a job portfolio: each file is
self-contained, standard library only, and prints a short
proof of what it does when run. No real credentials, no
network calls to external sites, no copied product code —
the security, ledger, and spiking-network files are small
teaching models written from first principles.

Run one: `python3 01_binary_search.py`
Run all: `for f in *.py; do python3 "$f" || echo "FAILED: $f"; done`

1. Binary search, manual and with bisect — `01_binary_search.py`
2. Merge sort and quick sort, verified against sorted() — `02_sorting.py`
3. Singly linked list: insert, delete, reverse — `03_linked_list.py`
4. Stack (LIFO) and queue (FIFO) done the right way — `04_stack_queue.py`
5. Hash map with chaining and resizing, built from scratch — `05_hash_map.py`
6. Graph BFS/DFS and shortest path with parent tracking — `06_graph_search.py`
7. Dynamic programming: memoized Fibonacci, min coin change — `07_dynamic_programming.py`
8. Recursion done carefully: factorial, tree sum, Tower of Hanoi — `08_recursion.py`
9. Slow salted password hashing (PBKDF2) with timing-safe verify — `09_password_hashing.py`
10. Message authentication with HMAC-SHA256 — `10_hmac_signing.py`
11. Input validation at the boundary, reject the rest — `11_input_validation.py`
12. Token bucket rate limiting vs fixed-window bursts — `12_rate_limiter.py`
13. Log redaction by field name, before writing — `13_log_redaction.py`
14. Safe path joining that stops directory traversal — `14_safe_paths.py`
15. Constant-time secret comparison with hmac.compare_digest — `15_timing_compare.py`
16. SQLite CRUD with parameterized queries — `16_sqlite_crud.py`
17. SQLite transactions: atomic transfer, rollback on overdraft — `17_sqlite_transactions.py`
18. SQLite online backup with verified restore — `18_sqlite_backup.py`
19. Defensive CSV parsing: bad rows skipped and counted — `19_csv_parsing.py`
20. JSON handling with validation and safe defaults — `20_json_handling.py`
21. Tiny REST-style API on the standard library — `21_http_server_api.py`
22. HTTP client retry with backoff, only on retryable statuses — `22_http_retry_client.py`
23. Pagination without skipping or repeating items — `23_pagination.py`
24. API payload validation reporting every error at once — `24_api_validation.py`
25. Threading race condition, then the lock that fixes it — `25_threading_counter.py`
26. Thread pool with ordered results and isolated failures — `26_thread_pool.py`
27. Producer/consumer queue with sentinel shutdown — `27_producer_consumer.py`
28. Asyncio concurrency: three slow tasks in the time of one — `28_asyncio_demo.py`
29. Multiprocessing for CPU work across processes — `29_multiprocessing_demo.py`
30. File watcher by polling with a mid-run detection proof — `30_file_watcher.py`
31. Configuration: defaults, file, then environment overrides — `31_config_loader.py`
32. CLI tool with argparse subcommands, tested in-process — `32_cli_tool.py`
33. Log rotation that bounds disk use, newest lines survive — `33_log_rotation.py`
34. Zip archive creation with verified contents — `34_zip_archiver.py`
35. Temporary files that clean up even on exception — `35_temp_files.py`
36. Unit tests with unittest, run and reported in-process — `36_unittest_example.py`
37. Property-style checks: invariants over many cases — `37_property_checks.py`
38. Mocking external services with unittest.mock — `38_mock_demo.py`
39. LRU cache with recency refresh and eviction — `39_lru_cache.py`
40. Job queue with retries and a dead-letter pile — `40_job_queue.py`
41. Hash-chained audit log, tamper-evident — `41_audit_chain.py`
42. Bloom filter: no false negatives, sizing controls false positives — `42_bloom_filter.py`
43. Circuit breaker: stop calling a failing service — `43_circuit_breaker.py`
44. Idempotency keys: retries never double-apply — `44_idempotency.py`
45. Publish/subscribe event bus with fault isolation — `45_event_bus.py`
46. Leaky integrate-and-fire neuron simulation — `46_leaky_neuron.py`
47. STDP weight update rule, teaching size — `47_stdp_demo.py`
48. Reservoir projection plus trainable perceptron readout — `48_reservoir_readout.py`
49. Binary packet header parsing with struct and validation — `49_packet_parser.py`
50. Frequency-band power from a synthetic signal — `50_signal_bands.py`
