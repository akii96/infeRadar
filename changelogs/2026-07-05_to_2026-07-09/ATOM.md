# ATOM: PR digest (2026-07-05 to 2026-07-09)

_45 merged, 25 newly opened - source ROCm/ATOM, generated 2026-07-09T12:19:19Z_

## TL;DR
- **DeepSeek V4 and GLM 5.2 dominated the window**, with major engineering focus on Multi-Token Prediction (MTP) adaptation, sparse attention optimizations, and quantization.
- **DeepSeek V4 performance** saw merged Triton kernel optimizations for sparse prefill attention and newly opened work on FP4 activation quantization.
- **GLM 5.2 expanded its footprint** by gaining merged vLLM plugin support, alongside a massive newly opened PR wiring up its MTP capabilities.
- **MiniMax-M3 advanced** via merged SGLang plugin support, sparse vLLM metadata optimizations, and in-progress EAGLE3 speculative decoding.
- **Distributed routing and infrastructure** improved with an in-progress native scale-up KV connector using HIP VMM and merged Spur cluster benchmark integrations.

## Most important PRs
- **[#1372](https://github.com/ROCm/ATOM/pull/1372)** Adapts DeepSeek V4 Multi-Token Prediction (MTP) for the vLLM plugin, enabling advanced speculative decoding paths for the model.
- **[#1498](https://github.com/ROCm/ATOM/pull/1498)** Optimizes the DeepSeek V4 sparse prefill attention Triton kernel, significantly improving prefill performance.
- **[#1395](https://github.com/ROCm/ATOM/pull/1395)** Introduces SGLang plugin support for MiniMax-M3, expanding the serving ecosystem for the M3 architecture.
- **[#1531](https://github.com/ROCm/ATOM/pull/1531)** (Newly opened) Wires up Multi-Token Prediction (MTP) for GLM 5.2 in the vLLM plugin, a major feature addition for the GLM family.
- **[#1499](https://github.com/ROCm/ATOM/pull/1499)** (Newly opened) Introduces a native scale-up KV connector using HIP VMM, improving distributed KV cache management and scaling.

## More changes by area

<details>
<summary>Performance (6)</summary>

- [#1493](https://github.com/ROCm/ATOM/pull/1493) chunked indexer and online topk to reduce the mem footprint of logits tensor for Sparse MLA
- [#1342](https://github.com/ROCm/ATOM/pull/1342) optimize sparse vLLM metadata for improved performance of vllm-atom
- [#1472](https://github.com/ROCm/ATOM/pull/1472) reuse persistent ubatch worker threads
- [#1464](https://github.com/ROCm/ATOM/pull/1464) adaptive BLOCK_K for csa_translate_pack on DeepSeek V4
- [#1537](https://github.com/ROCm/ATOM/pull/1537) Revert for DP Stablize perf
- [#1477](https://github.com/ROCm/ATOM/pull/1477) (Newly opened) Triton Walsh-Hadamard rotate_activation kernel
</details>

<details>
<summary>Kernels & attention (12)</summary>

- [#1514](https://github.com/ROCm/ATOM/pull/1514) (Newly opened) enable pcp for dsa models
- [#1518](https://github.com/ROCm/ATOM/pull/1518) (Newly opened) Support EAGLE3 spec decoding for MiniMax-M3
- [#1481](https://github.com/ROCm/ATOM/pull/1481) (Newly opened) Optimize GLM5.2 MTP
- [#1490](https://github.com/ROCm/ATOM/pull/1490) (Newly opened) wire split-K GEMM prezero into Kimi MLA/MoE decode via a torch.compile pass
- [#1473](https://github.com/ROCm/ATOM/pull/1473) (Newly opened) enable minimax m3 fp8 index cache and fuse index_score_kernel with partial_topk kernel
- [#1509](https://github.com/ROCm/ATOM/pull/1509) (Newly opened) pa_prefill_sparse for GFX12
- [#1526](https://github.com/ROCm/ATOM/pull/1526) (Newly opened) align TBO v4_batch_id_per_token buffer to int32
- [#1468](https://github.com/ROCm/ATOM/pull/1468) (Newly opened) run15 cu_seqlens_q stale probe (3-state dump + guard)
- [#1513](https://github.com/ROCm/ATOM/pull/1513) support glm5.2 in vllm plugin mode
- [#1409](https://github.com/ROCm/ATOM/pull/1409) align input norm quant with attention quant for Kimi
- [#1480](https://github.com/ROCm/ATOM/pull/1480) Fix sglang minimax m3 cuda graph capture problem
- [#1466](https://github.com/ROCm/ATOM/pull/1466) fix DeepSeek V4 FP8 indexer cache_scale per-layer aliasing
</details>

<details>
<summary>MoE & quantization (9)</summary>

- [#1494](https://github.com/ROCm/ATOM/pull/1494) enable ar+norm+quant fusion
- [#1496](https://github.com/ROCm/ATOM/pull/1496) support llama-405B quant type
- [#1479](https://github.com/ROCm/ATOM/pull/1479) (Newly opened) implement fp4_act_quant Triton kernel for DeepSeek-V4
- [#1488](https://github.com/ROCm/ATOM/pull/1488) (Newly opened) auto-degrade FP8 block_n/k from 128 to 64 on alignment mismatch
- [#1500](https://github.com/ROCm/ATOM/pull/1500) (Newly opened) online quantize weights when loading weights
- [#1525](https://github.com/ROCm/ATOM/pull/1525) (Newly opened) Satya/atom dsv4 stuff
- [#1504](https://github.com/ROCm/ATOM/pull/1504) (Newly opened) Enable GFX12 Preshuffle Weights
- [#1540](https://github.com/ROCm/ATOM/pull/1540) (Newly opened) update shuffle weight for gfx1250
- [#1527](https://github.com/ROCm/ATOM/pull/1527) (Newly opened) Fix DeepSeek V4 fused shared expert mapping
</details>

<details>
<summary>Model support (4)</summary>

- [#1454](https://github.com/ROCm/ATOM/pull/1454) enable prefix cache for deepseek v4
- [#1451](https://github.com/ROCm/ATOM/pull/1451) fix V4 OOM issue
- [#1489](https://github.com/ROCm/ATOM/pull/1489) avoid Qwen3-32B GSM8K truncation
- [#1436](https://github.com/ROCm/ATOM/pull/1436) fix qwen3.5 full decode graph error
</details>

<details>
<summary>Parallelism & scheduling (7)</summary>

- [#1447](https://github.com/ROCm/ATOM/pull/1447) Remove legacy proxy, update docs, and enhance scripts
- [#1517](https://github.com/ROCm/ATOM/pull/1517) fix: dpa kv transfer error on spur
- [#1505](https://github.com/ROCm/ATOM/pull/1505) (Newly opened) fix: dpa kv transfer error on spur
- [#1501](https://github.com/ROCm/ATOM/pull/1501) (Newly opened) Enable cache aware DP routing
- [#1495](https://github.com/ROCm/ATOM/pull/1495) (Newly opened) reserve prefill-activation headroom and size KV pool for the tightest TP rank
- [#1474](https://github.com/ROCm/ATOM/pull/1474) propagate dp_uniform_decode to TBO ubatches
- [#1503](https://github.com/ROCm/ATOM/pull/1503) Revert "[ATOM][Fix] propagate dp_uniform_decode to TBO ubatches"
</details>

<details>
<summary>CI, tests & build (23)</summary>

- [#1475](https://github.com/ROCm/ATOM/pull/1475) add Spur cluster benchmark support
- [#1461](https://github.com/ROCm/ATOM/pull/1461) publish benchmark data on dashboard
- [#1516](https://github.com/ROCm/ATOM/pull/1516) gate heavy PR tests by approval or label
- [#1476](https://github.com/ROCm/ATOM/pull/1476) add GLM5.2 MXFP4 MTP into nightly acc check and benchmark
- [#1519](https://github.com/ROCm/ATOM/pull/1519) publish ATOMesh benchmark data with MI350X/MI355X hardware tag on dashboard
- [#1487](https://github.com/ROCm/ATOM/pull/1487) replace brittle build_args golden with composition + smoke
- plus 17 more minor CI, benchmark, and test updates ([#1535](https://github.com/ROCm/ATOM/pull/1535), [#1485](https://github.com/ROCm/ATOM/pull/1485), [#1470](https://github.com/ROCm/ATOM/pull/1470), [#1478](https://github.com/ROCm/ATOM/pull/1478), [#1538](https://github.com/ROCm/ATOM/pull/1538), [#1524](https://github.com/ROCm/ATOM/pull/1524), [#1482](https://github.com/ROCm/ATOM/pull/1482), [#1523](https://github.com/ROCm/ATOM/pull/1523), [#1536](https://github.com/ROCm/ATOM/pull/1536), [#1533](https://github.com/ROCm/ATOM/pull/1533), [#1486](https://github.com/ROCm/ATOM/pull/1486), [#1508](https://github.com/ROCm/ATOM/pull/1508), [#1512](https://github.com/ROCm/ATOM/pull/1512), [#1528](https://github.com/ROCm/ATOM/pull/1528), [#1530](https://github.com/ROCm/ATOM/pull/1530), [#1529](https://github.com/ROCm/ATOM/pull/1529), [#1521](https://github.com/ROCm/ATOM/pull/1521))
</details>

<details>
<summary>Bugfixes (2)</summary>

- [#1510](https://github.com/ROCm/ATOM/pull/1510) Automatic orphan reaping so EngineCore/worker processes can't pin stale IPC/VRAM on parent exit
- [#1502](https://github.com/ROCm/ATOM/pull/1502) fix GLM5.2 n-shot100 accuracy
</details>

<details>
<summary>Refactors & Other (2)</summary>

- [#1539](https://github.com/ROCm/ATOM/pull/1539) Add review-pr Claude Code skill for ATOM PRs
- [#1522](https://github.com/ROCm/ATOM/pull/1522) dedup prefill density check and drop dead threshold attr
</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (ATOM.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 184ad1ff1142256752f0a4ee81d2dbfadf4c0248e6eb143d5815424b73184151 -->
