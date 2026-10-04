# ATOM: PR digest (2026-09-09 to 2026-09-13)

_32 merged, 22 newly opened - source ROCm/ATOM, generated 2026-09-13T23:23:46Z_

## TL;DR
- **Model attention:** DeepSeek-V4 (AITer comm-fused MoE merged, SGLang bridge fix merged, Engram n-gram lookup opened), GLM-5.2 (LMCache multiprocess offload, CPP4+DCP4 ATOMesh coverage), and MiniMax-M3 (decode and sparse-selection perf, FP8 NaN fix, CPU offload). Kimi-K3 also got a draft-block CUDA graph and agentic recipes.
- **Performance:** MiniMax-M3 decode index-score splitting (`[#2163](https://github.com/ROCm/ATOM/pull/2163)`) and kernel routing by row count (`[#2205](https://github.com/ROCm/ATOM/pull/2205)`) are merged. A dense paged decode workgroup split (`[#2179](https://github.com/ROCm/ATOM/pull/2179)`) and fixed-slot MegaMoE for small decode graphs (`[#2209](https://github.com/ROCm/ATOM/pull/2209)`) are open.
- **MLA, MoE and quantization:** FlyDSL `gather_kv_b_proj` landed behind a flag, with an FP8 MLA follow-up and an FP4 DSA sparse indexer opened. Also opened: EP16 wideep transport with modular fused MoE.
- **Direction:** Long-context and agentic serving, with KV offload, PD/DCP cache transfer, tool/Responses API support, and heavy ATOMesh CI and latency instrumentation.

## Most important PRs
**`[#2114](https://github.com/ROCm/ATOM/pull/2114)` AITer communication-fused MoE for DeepSeek-V4**
Fuses MoE dispatch/combine communication with the AITer expert compute for DSv4, cutting separate all2all overhead on the EP path.

**`[#2121](https://github.com/ROCm/ATOM/pull/2121)` MLA/Indexer cache transfer in P-CPP/D-DCP PD disaggregation**
Lets prefill context-parallel and decode DCP deployments move MLA and indexer KV caches between stages. This is a prerequisite for large-scale disaggregated MLA serving.

**`[#1953](https://github.com/ROCm/ATOM/pull/1953)` GLM-5.2 LMCache multiprocess offload**
Adds multiprocess KV offload for GLM-5.2, with AITER/MLA attention and distributed changes. Larger effective KV capacity for long contexts.

**`[#2163](https://github.com/ROCm/ATOM/pull/2163)` MiniMax-M3 decode index-score split bounded by blocks-per-chunk**
Bounds the sparse-attention decode index-score split so work is balanced across chunks. Companion `[#2205](https://github.com/ROCm/ATOM/pull/2205)` routes sparse selection to the Triton kernel that wins at a given row count.

**`[#2151](https://github.com/ROCm/ATOM/pull/2151)` Kimi-K3 dspark draft block captured in a CUDA graph**
Captures the speculative draft block in a CUDA graph, removing per-step launch overhead in speculative decode.

## More changes by area

<details>
<summary>Performance (3)</summary>

- [#2179](https://github.com/ROCm/ATOM/pull/2179) (open) split dense paged decode by workgroups for MiniMax-M3
- [#2209](https://github.com/ROCm/ATOM/pull/2209) (open) fixed-slot MegaMoE for small decode graphs
- [#2173](https://github.com/ROCm/ATOM/pull/2173) (open) pin the image Triton to the perf-good ROCm 3.7.0 build

</details>

<details>
<summary>Kernels & attention (5)</summary>

- [#2170](https://github.com/ROCm/ATOM/pull/2170) FlyDSL backend for `gather_kv_b_proj`
- [#2215](https://github.com/ROCm/ATOM/pull/2215) route the `kv_b_proj` gather by capability, not import success
- [#2191](https://github.com/ROCm/ATOM/pull/2191) (open) FP8 MLA on top of [#2170](https://github.com/ROCm/ATOM/pull/2170)
- [#2216](https://github.com/ROCm/ATOM/pull/2216) (open) score the DSA sparse indexer in FP4
- [#2199](https://github.com/ROCm/ATOM/pull/2199) (open) enable asm sparse prefill for V4 on gfx1250

</details>

<details>
<summary>MoE & quantization (5)</summary>

- [#2176](https://github.com/ROCm/ATOM/pull/2176) bound the all2all receive buffer by what the group sent; give TBO ubatches the map their gather needs
- [#2190](https://github.com/ROCm/ATOM/pull/2190) restore the AITER EP top-k tuning key for RCCL transport
- [#2182](https://github.com/ROCm/ATOM/pull/2182) drop topk from gfx1250 MegaMoE `recv_token_bound`
- [#2187](https://github.com/ROCm/ATOM/pull/2187) (open) integrate EP16 transport with modular fused MoE
- [#2195](https://github.com/ROCm/ATOM/pull/2195) (open) BF16 mHC computation and tracing copy fixes

</details>

<details>
<summary>Model support (5)</summary>

- [#2211](https://github.com/ROCm/ATOM/pull/2211) fix NaN from the maskless FP8 kernel in MiniMax-M3 (gqa=16, partial tail)
- [#1996](https://github.com/ROCm/ATOM/pull/1996) align the DeepSeek-V4 SGLang bridge with the geometry/dest_rows API
- [#2192](https://github.com/ROCm/ATOM/pull/2192) find the dspark stage count when `--model` names a hub repo
- [#2185](https://github.com/ROCm/ATOM/pull/2185) (open) host-side n-gram lookup (Engram) for DeepSeek-V4.1
- [#2212](https://github.com/ROCm/ATOM/pull/2212) (open) allow MTP8 with spec decode

</details>

<details>
<summary>Parallelism & scheduling (6)</summary>

- [#2166](https://github.com/ROCm/ATOM/pull/2166) release M3 offload blocks incrementally
- [#2175](https://github.com/ROCm/ATOM/pull/2175) M3 CPU offload cache optimization
- [#2201](https://github.com/ROCm/ATOM/pull/2201) (open) bound Dense/M3 saves with safe retirement
- [#2204](https://github.com/ROCm/ATOM/pull/2204) (open) failure channel and watermark rollback for DSv4 PAGE saves
- [#2196](https://github.com/ROCm/ATOM/pull/2196) (open) make the prefill coalescer work on the TP/DCP path
- [#2203](https://github.com/ROCm/ATOM/pull/2203) (open) match vLLM/SGLang ZMQ framing for KV events, with per-DP-rank port offset

</details>

<details>
<summary>API & serving (7)</summary>

- [#1955](https://github.com/ROCm/ATOM/pull/1955) vendor the tool parser implementation
- [#2178](https://github.com/ROCm/ATOM/pull/2178) support Codex custom and deferred tools in Responses
- [#2188](https://github.com/ROCm/ATOM/pull/2188) validate token limits and preserve thinking history in the OpenAI API
- [#2165](https://github.com/ROCm/ATOM/pull/2165) expose streaming ITL and API TTFT histograms in latency reports
- [#2169](https://github.com/ROCm/ATOM/pull/2169) freeze the startup heap and reuse the emitted delta
- [#2085](https://github.com/ROCm/ATOM/pull/2085) upgrade the vLLM OOT plugin to 0.28.0
- [#2183](https://github.com/ROCm/ATOM/pull/2183) (open) keep media prompts out of the prefix cache

</details>

<details>
<summary>CI & build (13)</summary>

- [#2177](https://github.com/ROCm/ATOM/pull/2177) report p90 latency and AIPerf raw metrics; support Kimi-K3 agentic CI
- [#2189](https://github.com/ROCm/ATOM/pull/2189) adapt ATOMesh to Crusoe v2 runners and candidate node scheduling
- [#2134](https://github.com/ROCm/ATOM/pull/2134) GLM-5.2 CPP4+DCP4 ATOMesh coverage
- [#2172](https://github.com/ROCm/ATOM/pull/2172) move the 1k/1k benchmark grid to a weekly cron
- [#2180](https://github.com/ROCm/ATOM/pull/2180) gate heavy tests on current review decision
- [#2181](https://github.com/ROCm/ATOM/pull/2181) fix shared model cache mount path for vLLM and SGLang
- [#2186](https://github.com/ROCm/ATOM/pull/2186) (open) metrics enhancements for scheduler, cache, and decoding
- [#2197](https://github.com/ROCm/ATOM/pull/2197) (open) align the wheel release with aiter
- [#2198](https://github.com/ROCm/ATOM/pull/2198) (open) pin Mooncake v0.3.14-rc1 and disable HIP DMA-BUF by default
- [#2193](https://github.com/ROCm/ATOM/pull/2193) (open) ATOMesh single-node benchmark selection
- [#2168](https://github.com/ROCm/ATOM/pull/2168) (open) close the engine in the examples; let the release golden diff fail
- [#2206](https://github.com/ROCm/ATOM/pull/2206) (open) set `HSA_ENABLE_IPC_MODE_LEGACY=1` to avoid GPU memory pin
- [#2207](https://github.com/ROCm/ATOM/pull/2207) (open) default `ATOM_USE_FLYDSL_GATHER_KV_B_PROJ` to false

</details>

<details>
<summary>Docs (4)</summary>

- [#2174](https://github.com/ROCm/ATOM/pull/2174) retarget the M3 agentic recipe to the InferenceX-aligned operating point
- [#2184](https://github.com/ROCm/ATOM/pull/2184) M3 agentic recipe: drop `use_index_cache`, add 48c CPU offload
- [#2208](https://github.com/ROCm/ATOM/pull/2208) Kimi-K3 AgentX per-concurrency params from the 12-point MI355X sweep
- [#2213](https://github.com/ROCm/ATOM/pull/2213) Kimi-K3 AgentX: C72 and C80 bands, drop the C14 CUDA-graph pin

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (ATOM.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: af1205043648f71fc5b45ff7cce564870244085330968dddff987250c8bf9962 -->
