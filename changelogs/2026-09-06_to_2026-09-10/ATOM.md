# ATOM: PR digest (2026-09-06 to 2026-09-10)

_25 merged, 26 newly opened - source ROCm/ATOM, generated 2026-09-10T13:57:23Z_

## TL;DR
- **Model focus:** DeepSeek-V4 got the most model-specific work. Merged [#2114](https://github.com/ROCm/ATOM/pull/2114) adds AITer communication-fused MoE, and the open [#2149](https://github.com/ROCm/ATOM/pull/2149) (V4-Flash-Vision) and [#2185](https://github.com/ROCm/ATOM/pull/2185) (engram n-gram lookup) extend the family. GLM-5.x work is all open (MTP in [#2157](https://github.com/ROCm/ATOM/pull/2157), agentic and PD recipes). MiniMax-M3 and Kimi-K3 also saw heavy work.
- **MoE and communication:** [#2110](https://github.com/ROCm/ATOM/pull/2110) merged a native RCCL DEP transport for MoE. [#2176](https://github.com/ROCm/ATOM/pull/2176) bounds the all2all receive buffer. Open [#2187](https://github.com/ROCm/ATOM/pull/2187) adds an EP16 wide-EP backend, and [#2190](https://github.com/ROCm/ATOM/pull/2190) restores the AITER EP top-k tuning key.
- **Decode and frontend perf:** MiniMax-M3 decode index-score split ([#2163](https://github.com/ROCm/ATOM/pull/2163)) merged, and a dense paged-decode workgroup split ([#2179](https://github.com/ROCm/ATOM/pull/2179)) is open. Frontend token coalescing ([#2161](https://github.com/ROCm/ATOM/pull/2161)) and a startup heap freeze ([#2169](https://github.com/ROCm/ATOM/pull/2169)) merged. Open [#2158](https://github.com/ROCm/ATOM/pull/2158) adds shortest-job-first prefill admission to cut p90 TTFT.
- **KV and disaggregation:** [#2147](https://github.com/ROCm/ATOM/pull/2147) restructured the KV pools, [#2121](https://github.com/ROCm/ATOM/pull/2121) added MLA/Indexer cache transfer for P-CPP/D-DCP, and CPU offload for M3 was optimized ([#2166](https://github.com/ROCm/ATOM/pull/2166), [#2175](https://github.com/ROCm/ATOM/pull/2175), [#2140](https://github.com/ROCm/ATOM/pull/2140)). Kimi-K3 P/D disaggregation is open in [#2154](https://github.com/ROCm/ATOM/pull/2154).
- **Direction:** Long-context agentic serving (KV offload, PD disaggregation, MTP) plus the benchmarking and latency tooling to measure it.

## Most important PRs
**[#2147](https://github.com/ROCm/ATOM/pull/2147) – refactor(kv-cache): one declaration per fact about the KV pools**
A 94-file refactor that makes each KV-pool property declared once, across attention, MLA, quantization, speculative decode and the plugin. It underpins the offload and PD work built on top.

**[#2110](https://github.com/ROCm/ATOM/pull/2110) – [MoE] Add native RCCL DEP transport**
Adds a native RCCL data/expert-parallel transport for MoE dispatch/combine, so MoE communication no longer depends on other all2all backends. [#2176](https://github.com/ROCm/ATOM/pull/2176) and the open [#2190](https://github.com/ROCm/ATOM/pull/2190) refine it.

**[#2114](https://github.com/ROCm/ATOM/pull/2114) – feat(dsv4): add AITer communication-fused MoE**
Fuses communication into the AITER MoE path for DeepSeek-V4, cutting separate dispatch/combine overhead.

**[#2121](https://github.com/ROCm/ATOM/pull/2121) – [ATOM][PD][DCP] Support MLA/Indexer cache transfer in P-CPP/D-DCP**
Lets prefill-decode disaggregation move MLA and indexer caches between prefill context-parallel and decode DCP groups. This is needed for disaggregated serving of MLA models.

**[#2163](https://github.com/ROCm/ATOM/pull/2163) – [Perf][MiniMax-M3] Bound the decode index-score split by blocks-per-chunk**
Bounds the decode index-score split so the kernel does not over-split on long contexts, improving M3 decode attention.

## More changes by area

<details>
<summary>Performance (4)</summary>

- [#2161](https://github.com/ROCm/ATOM/pull/2161) coalesce tokens before detokenization to reduce frontend stalls
- [#2169](https://github.com/ROCm/ATOM/pull/2169) freeze the startup heap and reuse the emitted delta
- [#2130](https://github.com/ROCm/ATOM/pull/2130) make the Kimi-K3 KDA temporal state dtype configurable
- [#2173](https://github.com/ROCm/ATOM/pull/2173) (open) pin the image Triton to the perf-good ROCm build

</details>

<details>
<summary>Kernels & attention (4)</summary>

- [#2179](https://github.com/ROCm/ATOM/pull/2179) (open) split MiniMax-M3 dense paged decode by workgroups
- [#2170](https://github.com/ROCm/ATOM/pull/2170) (open) add a flydsl backend for gather_kv_b_proj
- [#2191](https://github.com/ROCm/ATOM/pull/2191) (open) FP8 MLA on top of PR 2170
- [#2151](https://github.com/ROCm/ATOM/pull/2151) capture the Kimi-K3 DSpark draft block into a CUDA graph

</details>

<details>
<summary>MoE & quantization (3)</summary>

- [#2176](https://github.com/ROCm/ATOM/pull/2176) bound the all2all receive buffer and give TBO ubatches the map their gather needs
- [#2182](https://github.com/ROCm/ATOM/pull/2182) drop topk from the gfx1250 MegaMoE recv_token_bound
- [#2187](https://github.com/ROCm/ATOM/pull/2187) (open) minimal eager EP16 wide-EP backend

</details>

<details>
<summary>Model support (6)</summary>

- [#2149](https://github.com/ROCm/ATOM/pull/2149) (open) DeepSeek-V4-Flash-Vision support
- [#2185](https://github.com/ROCm/ATOM/pull/2185) (open) host-side engram n-gram lookup for DeepSeek-V4.1
- [#2157](https://github.com/ROCm/ATOM/pull/2157) (open) GLM-5.3-Flash MTP support
- [#2154](https://github.com/ROCm/ATOM/pull/2154) (open) Kimi-K3 P/D disaggregation
- [#2164](https://github.com/ROCm/ATOM/pull/2164) GLM-5.2 low-concurrency agentic cases with MTP adjustments
- [#2085](https://github.com/ROCm/ATOM/pull/2085) upgrade the OOT plugin to vLLM 0.28.0

</details>

<details>
<summary>Parallelism & scheduling (5)</summary>

- [#2166](https://github.com/ROCm/ATOM/pull/2166) release M3 offload blocks incrementally
- [#2175](https://github.com/ROCm/ATOM/pull/2175) M3 CPU offload cache optimization
- [#2140](https://github.com/ROCm/ATOM/pull/2140) PAGE-only m3 layout for MiniMax-M3 offload
- [#2146](https://github.com/ROCm/ATOM/pull/2146) (open) drive byte-level KV offload from the vLLM plugin via LMCache
- [#2158](https://github.com/ROCm/ATOM/pull/2158) (open) shortest-job-first prefill admission to cut p90 TTFT

</details>

<details>
<summary>API & serving (5)</summary>

- [#1955](https://github.com/ROCm/ATOM/pull/1955) vendor tool parser implementation
- [#2165](https://github.com/ROCm/ATOM/pull/2165) expose streaming ITL and API TTFT histograms in latency reports
- [#2178](https://github.com/ROCm/ATOM/pull/2178) (open) Codex custom and deferred tools in responses
- [#2188](https://github.com/ROCm/ATOM/pull/2188) (open) validate token limits and preserve thinking history
- [#2186](https://github.com/ROCm/ATOM/pull/2186) (open) metrics for scheduler, cache and decoding

</details>

<details>
<summary>Tests (1)</summary>

- [#2167](https://github.com/ROCm/ATOM/pull/2167) (open) preserve incremental offload and improve lifecycle regression tests

</details>

<details>
<summary>CI & build (10)</summary>

- [#2155](https://github.com/ROCm/ATOM/pull/2155) upload AIPerf Perfetto traces from benchmark workflows
- [#2177](https://github.com/ROCm/ATOM/pull/2177) p90 latency and AIPerf raw metrics in benchmark summary, kimi-k3 agentic CI
- [#2172](https://github.com/ROCm/ATOM/pull/2172) move the 1k/1k grid to a weekly cron
- [#2180](https://github.com/ROCm/ATOM/pull/2180) gate heavy tests on the current review decision
- [#2152](https://github.com/ROCm/ATOM/pull/2152) (open) opt-in paired performance check for PRs (ci:perf)
- [#2150](https://github.com/ROCm/ATOM/pull/2150) (open) ROCm 10 base image and wheel release flow
- [#2189](https://github.com/ROCm/ATOM/pull/2189) (open) adapt ATOMesh to Crusoe v2 runners
- [#2156](https://github.com/ROCm/ATOM/pull/2156) (open) set ATOM_GC_THRESHOLD for the EPLB MegaMoE c=4096 bench
- [#2181](https://github.com/ROCm/ATOM/pull/2181) (open) fix the shared model cache mount path for vLLM and SGLang
- [#2168](https://github.com/ROCm/ATOM/pull/2168) (open) close the engine in the examples and let the release golden diff fail

</details>

<details>
<summary>Docs (3)</summary>

- [#2174](https://github.com/ROCm/ATOM/pull/2174) retarget the M3 agentic recipe on the InferenceX aligned operating point
- [#2184](https://github.com/ROCm/ATOM/pull/2184) M3 agentic InferenceX recipe: drop use_index_cache, add 48c CPU offload
- [#2153](https://github.com/ROCm/ATOM/pull/2153) (open) GLM-5.2 AgentX PD recipe

</details>

<details>
<summary>Bugfixes (4)</summary>

- [#2148](https://github.com/ROCm/ATOM/pull/2148) fix negative pad-row KV length in MTP draft decode metadata
- [#2160](https://github.com/ROCm/ATOM/pull/2160) (open) fix the K3 DSpark MLA head-width, breakable-cudagraph eager break and fused Markov argmax NaN escape
- [#2183](https://github.com/ROCm/ATOM/pull/2183) (open) keep media prompts out of the prefix cache
- [#2192](https://github.com/ROCm/ATOM/pull/2192) (open) find the DSpark stage count when --model names a hub repo

</details>

<details>
<summary>Other (1)</summary>

- [#2190](https://github.com/ROCm/ATOM/pull/2190) (open) restore the AITER EP top-k tuning key for the RCCL transport

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (ATOM.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 042e61b89bfd6d1fca68541439d817b9e78e389e70b01ebcca3099e5995201aa -->
