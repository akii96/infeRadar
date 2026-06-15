# ATOM: PR digest (2026-06-10 to 2026-06-14)

_42 merged, 18 newly opened - source ROCm/ATOM, generated 2026-06-14T22:31:25Z_

## TL;DR
*   **DeepSeek v4 dominates:** Massive architectural features landed for DeepSeek v4, including Atomesh Prefill-Decode (PD) disaggregation, Multi-Token Prediction (MTP) support, and Token-midpoint Batch Optimization (TBO) for prefill micro-batch splitting.
*   **Plugin expansion:** Heavy expansion of both SGLang and vLLM plugins to support new models, notably Kimi-K2.6-MXFP4, GLM5, MiniMax-M2.5, and Mimo-v2.5-Pro.
*   **MoE & Quantization wins:** Significant kernel upgrades landed for w4 MoE using AITER Triton kernels, alongside new online quantization support for both vLLM and SGLang plugins.
*   **Hardware targeting:** GFX1250 and MI350X are seeing targeted bring-up, including MI350X preflight CI and GFX1250-specific a8w4 MoE and Triton GEMM optimizations.

## Most important PRs
*   **[#1194](https://github.com/ROCm/ATOM/pull/1194)** Enables DeepSeek v4 Multi-Token Prediction (MTP) and integrates Atomesh for Prefill-Decode (PD) disaggregation. This is a major architectural step for scaling DeepSeek v4 inference across distributed meshes.
*   **[#1142](https://github.com/ROCm/ATOM/pull/1142)** Implements Token-midpoint Batch Optimization (TBO) for DeepSeek v4, splitting prefill micro-batches to improve attention and MLA pipeline utilization.
*   **[#1044](https://github.com/ROCm/ATOM/pull/1044)** Integrates AITER-based Triton kernels for INT4/FP4 Mixture of Experts (MoE). This replaces older paths to significantly improve w4 MoE throughput and memory bandwidth utilization.
*   **[#1191](https://github.com/ROCm/ATOM/pull/1191)** (Open) A massive +6.8k line PR to enable MiniMax-M3 support within the vLLM ATOM plugin, wiring up its specific attention and MoE routing requirements.
*   **[#1163](https://github.com/ROCm/ATOM/pull/1163)** Fuses QK-norm, all-reduce, RoPE, group quantization, and cache shuffle-write into a single kernel for MiniMax models, drastically reducing memory round-trips and kernel launch overhead.

## More changes by area

<details>
<summary>Performance (1)</summary>

- [#1140](https://github.com/ROCm/ATOM/pull/1140) Fuses mhc_post/pre by using hc_state to transfer hidden_state and residual between layers
</details>

<details>
<summary>Kernels & attention (9)</summary>

- [#1175](https://github.com/ROCm/ATOM/pull/1175) Fixes Xyt/minimax qknorm all-reduce
- [#1144](https://github.com/ROCm/ATOM/pull/1144) Forces block_size for Unified Attention on GFX12 and resolves prefill bug
- [#1206](https://github.com/ROCm/ATOM/pull/1206) Sinks GPT-OSS prefill to ASM local
- [#1180](https://github.com/ROCm/ATOM/pull/1180) Supports MiniMax TP1 qknorm RoPE fusion
- [#1198](https://github.com/ROCm/ATOM/pull/1198) Disables Triton KV projection GEMM for GFX1250
- [#1183](https://github.com/ROCm/ATOM/pull/1183) (Open) Supports kv_buffer shuffled MLA for GFX12 via Triton/Gluon
- [#1152](https://github.com/ROCm/ATOM/pull/1152) (Open) Adds support for chunked long prefill
- [#1182](https://github.com/ROCm/ATOM/pull/1182) (Open) Sinks 450 full prefill to ASM
- [#1209](https://github.com/ROCm/ATOM/pull/1209) (Open) Fixes MHA PagedAttention ASM metadata alignment
</details>

<details>
<summary>MoE & quantization (10)</summary>

- [#975](https://github.com/ROCm/ATOM/pull/975) Updates SGLang-ATOM DeepSeek FP4 recipe
- [#1153](https://github.com/ROCm/ATOM/pull/1153) Enables FP8 prefill for FP4 v2 models in SGLang
- [#1055](https://github.com/ROCm/ATOM/pull/1055) Fuses input_rmsnorm_quant and qknorm_quant for DeepSeek v2
- [#1169](https://github.com/ROCm/ATOM/pull/1169) Implements MiniMax all-reduce RMSNorm quantization
- [#1157](https://github.com/ROCm/ATOM/pull/1157) Supports online quantization for vLLM plugin mode
- [#1172](https://github.com/ROCm/ATOM/pull/1172) Enables online quantization in SGLang ATOM
- [#1177](https://github.com/ROCm/ATOM/pull/1177) Removes unnecessary FP8 scale for vLLM plugin
- [#1155](https://github.com/ROCm/ATOM/pull/1155) Fixes incorrect layerwise-share-expert-fusion in MoE
- [#1150](https://github.com/ROCm/ATOM/pull/1150) (Open) Implements MiniMax all-reduce RMSNorm quantization
- [#1176](https://github.com/ROCm/ATOM/pull/1176) (Open) Removes unnecessary FP8 scale for vLLM plugin
</details>

<details>
<summary>Model support (9)</summary>

- [#1195](https://github.com/ROCm/ATOM/pull/1195) Enables Kimi-K2.6-MXFP4 in SGLang ATOM
- [#1145](https://github.com/ROCm/ATOM/pull/1145) Supports GLM5 in SGLang plugin
- [#1170](https://github.com/ROCm/ATOM/pull/1170) Supports MiniMax-M2.5 in SGLang plugin
- [#654](https://github.com/ROCm/ATOM/pull/654) Supports Mimo-v2.5-Pro and Mimo PD disaggregation with Mooncake
- [#1189](https://github.com/ROCm/ATOM/pull/1189) Registers Kimi-K2.5 for the SGLang plugin path
- [#1204](https://github.com/ROCm/ATOM/pull/1204) (Open) Launches DeepSeek v4 for ATOM SGLang
- [#1185](https://github.com/ROCm/ATOM/pull/1185) (Open) Adds DeepSeek v4 support for SGLang plugin
- [#1196](https://github.com/ROCm/ATOM/pull/1196) (Open) Optimizes DeepSeek v4 metadata build for vLLM
- [#1201](https://github.com/ROCm/ATOM/pull/1201) (Open) Supports Eagle 3.1 speculative decoding in vLLM-ATOM
</details>

<details>
<summary>Parallelism & scheduling (2)</summary>

- [#1193](https://github.com/ROCm/ATOM/pull/1193) (Open) Enables true TP=8 for Kimi-K2.5 in SGLang plugin
- [#1166](https://github.com/ROCm/ATOM/pull/1166) (Open) Enables multistream for DeepSeek v4 in vLLM
</details>

<details>
<summary>Hardware & arch (1)</summary>

- [#1202](https://github.com/ROCm/ATOM/pull/1202) Refactors GFX1250 a8w4 MoE, Triton RMSNorm, and Triton GEMM for GPT-OSS
</details>

<details>
<summary>API & serving (2)</summary>

- [#1147](https://github.com/ROCm/ATOM/pull/1147) Adds kv_transfer_params support to `/v1/chat/completions` for PD disaggregation
- [#1184](https://github.com/ROCm/ATOM/pull/1184) (Open) Supports Kimi-K2.6 `/v1/messages` API with prompt caching enabled
</details>

<details>
<summary>Bugfixes (6)</summary>

- [#1208](https://github.com/ROCm/ATOM/pull/1208) Corrects TBO and DP-attention accuracy regression in v4
- [#1154](https://github.com/ROCm/ATOM/pull/1154) Fixes DeepSeek v4 accuracy in vLLM plugin
- [#1165](https://github.com/ROCm/ATOM/pull/1165) Fixes model runner v2 for GEMM
- [#1167](https://github.com/ROCm/ATOM/pull/1167) Fixes model runner v2 for GEMM
- [#1162](https://github.com/ROCm/ATOM/pull/1162) Recovers GPT-OSS model runner v2 following AITER fix
- [#1146](https://github.com/ROCm/ATOM/pull/1146) Checks for None slot_mapping during dummy execution
</details>

<details>
<summary>CI & build (14)</summary>

- [#1139](https://github.com/ROCm/ATOM/pull/1139) Adds MI350X GPU preflight checks
- [#1159](https://github.com/ROCm/ATOM/pull/1159) (Open) Adds Atomesh accuracy and benchmark workflows
- [#1190](https://github.com/ROCm/ATOM/pull/1190) (Open) Fetches config from JSON for vLLM nightly accuracy
- [#1171](https://github.com/ROCm/ATOM/pull/1171) (Open) Adds DeepSeek v3.2 and GLM5.1 benchmarks
- [#1203](https://github.com/ROCm/ATOM/pull/1203) (Open) Updates Triton version in SGLang Docker for DeepSeek v4
- plus 9 more minor CI updates ([#1099](https://github.com/ROCm/ATOM/pull/1099), [#1151](https://github.com/ROCm/ATOM/pull/1151), [#1158](https://github.com/ROCm/ATOM/pull/1158), [#1164](https://github.com/ROCm/ATOM/pull/1164), [#1173](https://github.com/ROCm/ATOM/pull/1173), [#1178](https://github.com/ROCm/ATOM/pull/1178), [#1197](https://github.com/ROCm/ATOM/pull/1197), [#1199](https://github.com/ROCm/ATOM/pull/1199), [#1200](https://github.com/ROCm/ATOM/pull/1200))
</details>

<details>
<summary>Docs (1)</summary>

- [#1174](https://github.com/ROCm/ATOM/pull/1174) Updates ATOMesh license compliance
</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (ATOM.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
