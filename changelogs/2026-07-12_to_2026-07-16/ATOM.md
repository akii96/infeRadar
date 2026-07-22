# ATOM: PR digest (2026-07-12 to 2026-07-16)

_25 merged, 26 newly opened - source ROCm/ATOM, generated 2026-07-16T11:26:12Z_

## TL;DR
*   **DeepSeek-V4 and GLM 5.2** dominated this cycle. Major in-flight work for DeepSeek-V4 targets FP8 KV caching, FP4 Cross-Sequence Attention (CSA) indexing on gfx950, and MoRIIO write-push KV transfers for scale-up.
*   **GLM 5.2** saw heavy optimization, with merged Multi-Token Prediction (MTP) improvements and new FP8/MXFP4 support landing in the SGLang plugin.
*   **Memory & Serving:** Critical stability improvements were merged, ensuring the frontend immediately aborts engine requests and frees leaked KV cache upon client disconnects to prevent OOMs during streaming.
*   **Quantization:** Low-precision support continues to expand, with merged `per_block_fp8` online quantization and in-progress alignment for MXFP4 activation quantization rounding with Quark offline calibration.

## Most important PRs
*   **[#1531](https://github.com/ROCm/ATOM/pull/1531)** (Merged) Optimizes Multi-Token Prediction (MTP) for GLM 5.2. This significantly improves speculative decoding throughput by streamlining the AITer backend and MLA attention paths.
*   **[#1594](https://github.com/ROCm/ATOM/pull/1594)** (Opened) Introduces MoRIIO write-push KV transfer for DeepSeek-V4. This enables highly efficient cross-node KV cache synchronization over the fabric backend, critical for scale-up distributed inference.
*   **[#1581](https://github.com/ROCm/ATOM/pull/1581)** (Opened) Implements an FP4 Cross-Sequence Attention (CSA) indexer specifically optimized for the gfx950 architecture. This pushes DeepSeek-V4 memory compression further while maintaining indexing performance on AMD hardware.
*   **[#1611](https://github.com/ROCm/ATOM/pull/1611)** (Opened) Adds a prefill coalescer for Data Parallel (DP) attention. By batching prefill phases and adding Time-To-First-Token (TTFT) guards, this reduces overhead and improves latency for high-throughput serving.
*   **[#1589](https://github.com/ROCm/ATOM/pull/1589)** (Merged) Fixes a critical KV cache leak by ensuring the frontend aborts streaming sequences and frees memory immediately upon a real client disconnect, rather than waiting for normal completion.

## More changes by area

<details>
<summary>Kernels & attention (7)</summary>

- [#1606](https://github.com/ROCm/ATOM/pull/1606) (Opened) Aligns the GLM 5.2 attention path with ATOM in the SGLang plugin
- [#1599](https://github.com/ROCm/ATOM/pull/1599) (Opened) Optimizes GLM 5.2 Multi-Token Prediction (MTP) in ATOM SGLang
- [#1578](https://github.com/ROCm/ATOM/pull/1578) (Opened) Adds initial GLM 5.2 MTP support for ATOM SGLang
- [#1573](https://github.com/ROCm/ATOM/pull/1573) (Merged) Fixes SWA after paged-SWA migration for DeepSeek-V4 in SGLang/vLLM plugins
- [#1595](https://github.com/ROCm/ATOM/pull/1595) (Merged) Reconciles CUDA-graph padding in vLLM PIECEWISE attention for DeepSeek-V4
- [#1572](https://github.com/ROCm/ATOM/pull/1572) (Merged) Adds blockscale GEMM for DeepSeek-V4 on gfx1250 via FlyDSL
- [#1579](https://github.com/ROCm/ATOM/pull/1579) (Opened) Updates Triton MoE and kernel configurations for DeepSeek-V4 MLA

</details>

<details>
<summary>MoE & quantization (9)</summary>

- [#1600](https://github.com/ROCm/ATOM/pull/1600) (Opened) Implements FP8 KV cache support for DeepSeek-V4
- [#1576](https://github.com/ROCm/ATOM/pull/1576) (Merged) Adds GLM 5.2 FP8 and FP4 support to the SGLang plugin
- [#1411](https://github.com/ROCm/ATOM/pull/1411) (Merged) Supports `per_block_fp8` format for online quantization
- [#1601](https://github.com/ROCm/ATOM/pull/1601) (Opened) Aligns MXFP4 activation quantization rounding with Quark offline calibration
- [#1612](https://github.com/ROCm/ATOM/pull/1612) (Opened) Stabilizes ATOM FP8 no-eager rollout weight sync and CUDA graph lifecycle
- [#1570](https://github.com/ROCm/ATOM/pull/1570) (Opened) Wires GUGU activation and quantization fusion into Triton decode
- [#1584](https://github.com/ROCm/ATOM/pull/1584) (Opened) Fixes gfx94x load assert in MXFP4 MoE by enforcing single-source `use_triton_moe()`
- [#1610](https://github.com/ROCm/ATOM/pull/1610) (Opened) Fixes expert mapping logic in Triton MoE
- [#1614](https://github.com/ROCm/ATOM/pull/1614) (Opened) Adds architecture check for MoE bias interleaving

</details>

<details>
<summary>Model support & plugins (5)</summary>

- [#1587](https://github.com/ROCm/ATOM/pull/1587) (Opened) Upgrades vLLM plugin integration to v0.25.1
- [#1604](https://github.com/ROCm/ATOM/pull/1604) (Opened) Upgrades vLLM plugin integration to v0.25.1 (duplicate PR)
- [#1585](https://github.com/ROCm/ATOM/pull/1585) (Opened) Updates ATOM SGLang plugin for SGLang 0.5.15 compatibility
- [#1605](https://github.com/ROCm/ATOM/pull/1605) (Opened) Adds Eagle3 speculative decoding support for `gpt-oss-120b`
- [#1591](https://github.com/ROCm/ATOM/pull/1591) (Merged) Fixes DeepSeek-V4 SGLang index top-k metadata

</details>

<details>
<summary>Parallelism & scheduling (4)</summary>

- [#1603](https://github.com/ROCm/ATOM/pull/1603) (Opened) Adds multi-node Data Parallel (DP) support
- [#1586](https://github.com/ROCm/ATOM/pull/1586) (Opened) Fixes agentic dataset benchmark under Prefill-Decode (PD) disaggregation mode
- [#1575](https://github.com/ROCm/ATOM/pull/1575) (Merged) Adds Kimi-K2.5 MXFP4 PD disaggregation recipe and updates configurations
- [#1596](https://github.com/ROCm/ATOM/pull/1596) (Merged) Forces AITer unregistered collective capture path for DeepSeek-V4 DP+PIECEWISE

</details>

<details>
<summary>API & serving (2)</summary>

- [#1562](https://github.com/ROCm/ATOM/pull/1562) (Merged) Aborts engine requests on client disconnect to free leaked KV cache
- [#1597](https://github.com/ROCm/ATOM/pull/1597) (Merged) Allows using kebab-case for the `--kv-cache-dtype` CLI flag

</details>

<details>
<summary>Bugfixes & refactors (5)</summary>

- [#1615](https://github.com/ROCm/ATOM/pull/1615) (Opened) Refactors trace analysis for kernel and MoE profiling
- [#1571](https://github.com/ROCm/ATOM/pull/1571) (Opened) Fixes ATOM MTP memory fault in AITer backend
- [#1574](https://github.com/ROCm/ATOM/pull/1574) (Merged) Fixes ATOM native memory fault in AITer speculative decode path
- [#1549](https://github.com/ROCm/ATOM/pull/1549) (Merged) Fixes dispatch gap rule, arch-constant FP, and P5 timing errors
- [#1577](https://github.com/ROCm/ATOM/pull/1577) (Merged) Refactors AITer MLA attention codebase

</details>

<details>
<summary>CI, build & docs (14)</summary>

- [#1588](https://github.com/ROCm/ATOM/pull/1588) (Opened) Updates GLM-5.2 recipe documentation
- [#1566](https://github.com/ROCm/ATOM/pull/1566) (Merged) Adds MXFP4 intermediate variable and scheduler delay advice for Kimi-K2
- [#1607](https://github.com/ROCm/ATOM/pull/1607) (Opened) Updates GLM 5.2 FP8/MXFP4 recipe and benchmark configurations
- [#1613](https://github.com/ROCm/ATOM/pull/1613) (Opened) Modifies ATOM vLLM benchmark models
- [#1580](https://github.com/ROCm/ATOM/pull/1580) (Merged) Improves ATOMesh benchmark configuration and dashboard reporting
- plus 9 more minor CI, dashboard, and build environment updates ([#1457](https://github.com/ROCm/ATOM/pull/1457), [#1529](https://github.com/ROCm/ATOM/pull/1529), [#1567](https://github.com/ROCm/ATOM/pull/1567), [#1590](https://github.com/ROCm/ATOM/pull/1590), [#1592](https://github.com/ROCm/ATOM/pull/1592), [#1598](https://github.com/ROCm/ATOM/pull/1598), [#1602](https://github.com/ROCm/ATOM/pull/1602), [#1608](https://github.com/ROCm/ATOM/pull/1608), [#1609](https://github.com/ROCm/ATOM/pull/1609))

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (ATOM.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 62b317501f1eb1e3c62ad76d54d6a4d8765ace0b0016d0825e598a29c2141fc1 -->
