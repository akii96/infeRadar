# ATOM: PR digest (2026-06-03 to 2026-06-10)

_99 merged, 30 newly opened - source ROCm/ATOM, generated 2026-06-10T13:31:14Z_

## TL;DR
*   **DeepSeek & GPT-OSS Dominate:** DeepSeek (v4/v3.2) and GPT-OSS were the primary focus this cycle. Major performance wins include a 19.3% geomean speedup for DeepSeek v4 decode on MI355 (`sparse_attn_v4_paged_decode`) and new Token-Midpoint prefill micro-batch splitting (TBO) optimizations.
*   **Disaggregated Serving Architecture:** A massive architectural push towards disaggregated serving landed with the merge of the "Atomesh" PD (Prefill-Decode) router, enabling multi-node routing and KV cache transfer.
*   **Plugin Ecosystem (vLLM & SGLang):** Heavy updates to both plugins, including syncing Data Parallel / Expert Parallel (DP+EP) enablement for vLLM and a major attention backend refactor for SGLang to improve MLA integration.
*   **MoE & Quantization Expansion:** Expanded capabilities include layerwise shared expert fusion for all MoE models, DeepSeek v4 online quantization, and in-progress Triton MoE A8W4 support for GPT-OSS.
*   **Overall Direction:** The engine is rapidly maturing its multi-node disaggregated architecture (Atomesh) while aggressively optimizing DeepSeek v4/v3.2 execution on MI300/MI350 series hardware via fused kernels and advanced parallelism.

## Most important PRs
*   **[#919](https://github.com/ROCm/ATOM/pull/919)** Merges the core "Atomesh" routing layer for Prefill-Decode (PD) disaggregation. This enables multi-node KV cache transfer and distributed scheduling, forming the architectural foundation for next-generation disaggregated serving.
*   **[#1066](https://github.com/ROCm/ATOM/pull/1066)** Syncs Data Parallel and Expert Parallel (DP+EP) enablement into the vLLM plugin. This is critical for efficiently scaling massive MoE models like DeepSeek across multiple GPUs and nodes.
*   **[#1116](https://github.com/ROCm/ATOM/pull/1116)** Tunes the `sparse_attn_v4_paged_decode` kernel specifically for MI355 (gfx950). This targeted optimization delivers a massive 19.3% geomean performance improvement for DeepSeek v4 decode.
*   **[#1142](https://github.com/ROCm/ATOM/pull/1142)** Implements Token-Midpoint prefill micro-batch splitting (TBO) for DeepSeek v4. This optimizes compute and memory overlap during heavy prefill phases, significantly reducing latency.
*   **[#863](https://github.com/ROCm/ATOM/pull/863)** Executes a major structural refactor of the SGLang plugin's attention backend. This improves Multi-Head Latent Attention (MLA) integration and sets the stage for advanced sparse attention features.

## More changes by area

<details>
<summary>Performance (6)</summary>

- [#1140](https://github.com/ROCm/ATOM/pull/1140) Uses hc_state to transfer hidden_state and residual between layers for fused mhc_post/pre
- [#1038](https://github.com/ROCm/ATOM/pull/1038) Refines paged attention dispatch for better performance
- [#1047](https://github.com/ROCm/ATOM/pull/1047) Enables DeepSeek V3.2 quick reduce environments
- [#1048](https://github.com/ROCm/ATOM/pull/1048) Enables DeepSeek V3.2 quick reduce environments
- [#1137](https://github.com/ROCm/ATOM/pull/1137) (Newly opened) Adds a standalone model-loading (safetensors) speed benchmark
- [#1057](https://github.com/ROCm/ATOM/pull/1057) (Newly opened) Adds preshuffle logic for HIP fused_moe to improve performance

</details>

<details>
<summary>Kernels & attention (16)</summary>

- [#1163](https://github.com/ROCm/ATOM/pull/1163) Supports qknorm+allreduce+rope+group_quant+cache_shuffle_write fusion pattern for minimax
- [#1108](https://github.com/ROCm/ATOM/pull/1108) Adds Unified Attention support in Triton
- [#905](https://github.com/ROCm/ATOM/pull/905) Fails fast when page-size is less than KV element width
- [#954](https://github.com/ROCm/ATOM/pull/954) Separates Gated Delta Net (GDN) logic
- [#1079](https://github.com/ROCm/ATOM/pull/1079) Enables index cache feature for DSA models
- [#1051](https://github.com/ROCm/ATOM/pull/1051) Refines paged attention dispatch for minimax
- [#1112](https://github.com/ROCm/ATOM/pull/1112) Disables prefix cache in linear attention
- [#1058](https://github.com/ROCm/ATOM/pull/1058) Drops redundant cu_seqlens_q refill in attention metadata builder
- [#1046](https://github.com/ROCm/ATOM/pull/1046) Fixes MTP+DP speculative-num-steps > 1 error
- [#1104](https://github.com/ROCm/ATOM/pull/1104) (Newly opened) Adds 2D-tiled causal_conv1d prefill kernel for gated delta net
- [#1055](https://github.com/ROCm/ATOM/pull/1055) (Newly opened) Supports fused input_rmsnorm_quant & qknorm_quant for DeepSeek v2
- [#1152](https://github.com/ROCm/ATOM/pull/1152) (Newly opened) Supports chunk long prefill
- [#1153](https://github.com/ROCm/ATOM/pull/1153) (Newly opened) Implements FP8 prefill for FP4 v2 models in SGLang
- [#1054](https://github.com/ROCm/ATOM/pull/1054) (Newly opened) Restores missing concat+quant kernel for vLLM MLA
- [#1144](https://github.com/ROCm/ATOM/pull/1144) (Newly opened) Forces block_size for Unified Attention on GFX12
- [#1138](https://github.com/ROCm/ATOM/pull/1138) (Newly opened) Plans stream for specv2 in SGLang

</details>

<details>
<summary>MoE & quantization (19)</summary>

- [#958](https://github.com/ROCm/ATOM/pull/958) Supports layerwise shared expert fusion for all MoE models
- [#912](https://github.com/ROCm/ATOM/pull/912) Introduces online quantization documentation
- [#1027](https://github.com/ROCm/ATOM/pull/1027) Supports DeepSeek v4 online quantization
- [#1076](https://github.com/ROCm/ATOM/pull/1076) Fixes fused shared+routed MoE accuracy on DeepSeek-V4-Flash-Base
- [#963](https://github.com/ROCm/ATOM/pull/963) Implements fused qknorm + quant for DeepSeek v2
- [#875](https://github.com/ROCm/ATOM/pull/875) Enables Expert Parallelism (EP) for DeepSeek v4
- [#1088](https://github.com/ROCm/ATOM/pull/1088) Supports DeepSeek v4 DP+EP and fixes dump accuracy
- [#1087](https://github.com/ROCm/ATOM/pull/1087) Fixes EP for modular MoE
- [#1155](https://github.com/ROCm/ATOM/pull/1155) Fixes incorrect layerwise-share-expert-fusion
- [#1119](https://github.com/ROCm/ATOM/pull/1119) Fixes quant config read logic in model loading
- [#1132](https://github.com/ROCm/ATOM/pull/1132) Fixes MoE fallback route
- [#1077](https://github.com/ROCm/ATOM/pull/1077) Supports DeepSeek-V4-Flash-FP8 on gfx942
- [#1091](https://github.com/ROCm/ATOM/pull/1091) (Newly opened) Adds EP+pad support for Step-3.5-Flash-FP8
- [#1150](https://github.com/ROCm/ATOM/pull/1150) (Newly opened) Implements minimax allreduce rmsnorm quant
- [#1045](https://github.com/ROCm/ATOM/pull/1045) (Newly opened) Adds GPT-OSS Triton MoE A8W4 support
- [#1067](https://github.com/ROCm/ATOM/pull/1067) (Newly opened) Adds GPT-OSS Triton MoE A8W4 GEMM support
- [#1160](https://github.com/ROCm/ATOM/pull/1160) (Newly opened) Enables online_quant for vLLM-ATOM
- [#1157](https://github.com/ROCm/ATOM/pull/1157) (Newly opened) Supports online quantization for vLLM plugin mode
- [#1128](https://github.com/ROCm/ATOM/pull/1128) (Newly opened) Fixes fused shared expert in Qwen3.5-FP4

</details>

<details>
<summary>Model support (11)</summary>

- [#1060](https://github.com/ROCm/ATOM/pull/1060) Enables DeepSeek v4 in vLLM
- [#549](https://github.com/ROCm/ATOM/pull/549) Adds RLHF rollout integration support via verl
- [#1094](https://github.com/ROCm/ATOM/pull/1094) Supports DeepSeek v3.2 with SGLang plugin and sparse MLA
- [#943](https://github.com/ROCm/ATOM/pull/943) Adapts EAGLE 3.1 and adds Kimi K2.6 MLA draft
- [#1145](https://github.com/ROCm/ATOM/pull/1145) Supports GLM5 in SGLang plugin
- [#996](https://github.com/ROCm/ATOM/pull/996) Supports DeepSeek-V4-Flash-Base on gfx942
- [#1039](https://github.com/ROCm/ATOM/pull/1039) Adds DeepSeek-V3.2-mtp-ptpc for AW_P0 benchmark
- [#964](https://github.com/ROCm/ATOM/pull/964) Supports standalone draft model in SGLang
- [#1049](https://github.com/ROCm/ATOM/pull/1049) Enables dualstream in MTP
- [#1151](https://github.com/ROCm/ATOM/pull/1151) Adds temperature=0 for vLLM bench MTP models
- [#1126](https://github.com/ROCm/ATOM/pull/1126) (Newly opened) Adds DeepSeek R1 MXFP4 v2 recipe

</details>

<details>
<summary>Parallelism & scheduling (4)</summary>

- [#869](https://github.com/ROCm/ATOM/pull/869) Adds ZMQ publisher for KV cache events
- [#1121](https://github.com/ROCm/ATOM/pull/1121) Enables TBO compute/comm overlap in DeepSeek v4 and fixes mooncake gather hang
- [#1024](https://github.com/ROCm/ATOM/pull/1024) Fixes warmup to use full token budget for DP
- [#1101](https://github.com/ROCm/ATOM/pull/1101) (Newly opened) Supports DP and EP in vLLM plugin

</details>

<details>
<summary>Hardware & arch (2)</summary>

- [#1003](https://github.com/ROCm/ATOM/pull/1003) Fixes sparse_attn_v4_paged_prefill for MI308
- [#1149](https://github.com/ROCm/ATOM/pull/1149) (Newly opened) Adds bf16 gluon GEMM

</details>

<details>
<summary>API & serving (3)</summary>

- [#1086](https://github.com/ROCm/ATOM/pull/1086) Unifies engine utility command dispatch into EngineUtilityHandler
- [#1147](https://github.com/ROCm/ATOM/pull/1147) Adds kv_transfer_params support to /v1/chat/completions for PD disaggregation
- [#1129](https://github.com/ROCm/ATOM/pull/1129) (Newly opened) Formats and adds TLS for HTTP server

</details>

<details>
<summary>Refactors (2)</summary>

- [#1095](https://github.com/ROCm/ATOM/pull/1095) Renames atom-mesh to atomesh for brand alignment
- [#1120](https://github.com/ROCm/ATOM/pull/1120) Unifies cudagraph-vs-eager dispatch via ForwardMode

</details>

<details>
<summary>Bugfixes (10)</summary>

- [#1109](https://github.com/ROCm/ATOM/pull/1109) Fixes v4 TBO hang and hashes topk single all-gather
- [#1032](https://github.com/ROCm/ATOM/pull/1032) Fixes chunk prefill
- [#1072](https://github.com/ROCm/ATOM/pull/1072) Fixes DP EP failure in SGLang
- [#1059](https://github.com/ROCm/ATOM/pull/1059) Fixes v2 model launch issue in SGLang
- [#1162](https://github.com/ROCm/ATOM/pull/1162) Recovers model runner v2 for GPT-OSS due to AITer fix
- [#1146](https://github.com/ROCm/ATOM/pull/1146) Checks slot_mapping none for dummy execution
- [#1090](https://github.com/ROCm/ATOM/pull/1090) Fixes Kimi 2.5 issue
- [#1102](https://github.com/ROCm/ATOM/pull/1102) Fixes MHC fallback
- [#1154](https://github.com/ROCm/ATOM/pull/1154) (Newly opened) Fixes DeepSeek v4 accuracy in vLLM
- [#1165](https://github.com/ROCm/ATOM/pull/1165) (Newly opened) Fixes model runner v2 for GEMM

</details>

<details>
<summary>Tests, CI & build (44)</summary>

- [#1110](https://github.com/ROCm/ATOM/pull/1110) Unifies catalog matrix and fixes ROCm/CI quoting
- [#1006](https://github.com/ROCm/ATOM/pull/1006) Upgrades vLLM version to v0.22.0
- [#1050](https://github.com/ROCm/ATOM/pull/1050) Changes GPU memory utilization to 0.8 for gpt-oss-120b
- [#1159](https://github.com/ROCm/ATOM/pull/1159) (Newly opened) Adds Atomesh accuracy and benchmark workflows
- [#1124](https://github.com/ROCm/ATOM/pull/1124) (Newly opened) Adds v4 1p1d/2p1d slurm scripts with nightly docker image
- plus 39 more minor CI, benchmark, and docker updates including [#1093](https://github.com/ROCm/ATOM/pull/1093), [#975](https://github.com/ROCm/ATOM/pull/975), [#1005](https://github.com/ROCm/ATOM/pull/1005), [#1040](https://github.com/ROCm/ATOM/pull/1040), [#1080](https://github.com/ROCm/ATOM/pull/1080), [#1064](https://github.com/ROCm/ATOM/pull/1064), [#1135](https://github.com/ROCm/ATOM/pull/1135), [#1114](https://github.com/ROCm/ATOM/pull/1114), [#1134](https://github.com/ROCm/ATOM/pull/1134), [#1052](https://github.com/ROCm/ATOM/pull/1052), [#1113](https://github.com/ROCm/ATOM/pull/1113), [#1133](https://github.com/ROCm/ATOM/pull/1133), [#1062](https://github.com/ROCm/ATOM/pull/1062), [#1081](https://github.com/ROCm/ATOM/pull/1081), [#1107](https://github.com/ROCm/ATOM/pull/1107), [#1068](https://github.com/ROCm/ATOM/pull/1068), [#1097](https://github.com/ROCm/ATOM/pull/1097), [#1096](https://github.com/ROCm/ATOM/pull/1096), [#1065](https://github.com/ROCm/ATOM/pull/1065), [#1075](https://github.com/ROCm/ATOM/pull/1075), [#1084](https://github.com/ROCm/ATOM/pull/1084), [#1082](https://github.com/ROCm/ATOM/pull/1082), [#1123](https://github.com/ROCm/ATOM/pull/1123), [#1073](https://github.com/ROCm/ATOM/pull/1073), [#1158](https://github.com/ROCm/ATOM/pull/1158), [#1053](https://github.com/ROCm/ATOM/pull/1053), [#1074](https://github.com/ROCm/ATOM/pull/1074), [#1089](https://github.com/ROCm/ATOM/pull/1089), [#1127](https://github.com/ROCm/ATOM/pull/1127), [#1131](https://github.com/ROCm/ATOM/pull/1131), [#1071](https://github.com/ROCm/ATOM/pull/1071), [#1100](https://github.com/ROCm/ATOM/pull/1100), [#1106](https://github.com/ROCm/ATOM/pull/1106), [#1117](https://github.com/ROCm/ATOM/pull/1117), [#1118](https://github.com/ROCm/ATOM/pull/1118), [#1070](https://github.com/ROCm/ATOM/pull/1070), [#1139](https://github.com/ROCm/ATOM/pull/1139), [#1164](https://github.com/ROCm/ATOM/pull/1164), [#1099](https://github.com/ROCm/ATOM/pull/1099), [#1083](https://github.com/ROCm/ATOM/pull/1083)

</details>

<details>
<summary>Docs (2)</summary>

- [#1061](https://github.com/ROCm/ATOM/pull/1061) Fixes misattributed plugin PR citations in v0.1.3 release notes
- [#1063](https://github.com/ROCm/ATOM/pull/1063) Adds release notes for v0.1.3

</details>

<details>
<summary>Other (2)</summary>

- [#1031](https://github.com/ROCm/ATOM/pull/1031) Uses ATOM_USE_FP4_NON_SHUFFLE_TRITON_GEMM to enable non-shuffle Triton GEMM
- [#1105](https://github.com/ROCm/ATOM/pull/1105) Fixes DeepSeek v4 indexcache

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (ATOM.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
