# ATOM: PR digest (2026-06-03 to 2026-06-08)

_83 merged, 15 newly opened - source ROCm/ATOM, generated 2026-06-10T16:21:30Z_

## TL;DR
*   **DeepSeek (V4/V3.2) and GPT-OSS** models dominated this cycle, with a major focus on multi-node disaggregation, MoE routing, and quantization enablement.
*   A massive architectural shift landed with the **Atomesh PD (Prefill-Decode) disaggregation router**, enabling multi-node distributed inference and ZMQ-based KV cache event publishing.
*   **Significant kernel wins** include a 19.3% geomean speedup for `sparse_attn_v4_paged_decode` on MI355, and layerwise shared expert fusion across all MoE models.
*   **Integration matured rapidly**, with vLLM DPEP (Data Parallel + Expert Parallel) syncing to main, vLLM v0.22.0 upgrades, and a major SGLang attention refactor.

## Most important PRs
*   **[#919](https://github.com/ROCm/ATOM/pull/919)** introduces the Atomesh PD (Prefill-Decode) disaggregation router with multi-node support. This massive 61k-line architectural update enables distributed prefill and decode phases across nodes, integrating attention, LoRA, MLA, and quantization components for large-scale deployments.
*   **[#1066](https://github.com/ROCm/ATOM/pull/1066)** synchronizes Data Parallel and Expert Parallel (DPEP) enablement into the main vLLM-ATOM plugin. This provides critical distributed MoE and MLA routing capabilities for scaling large models across multiple GPUs.
*   **[#1116](https://github.com/ROCm/ATOM/pull/1116)** tunes the `sparse_attn_v4_paged_decode` kernel specifically for the MI355 (gfx950) architecture. This targeted optimization yields a 19.3% geomean performance improvement for decode attention.
*   **[#958](https://github.com/ROCm/ATOM/pull/958)** implements layerwise shared expert fusion across all Mixture of Experts (MoE) models. By fusing shared expert computations, it significantly reduces kernel launch overhead and improves memory bandwidth utilization during MoE routing.
*   **[#943](https://github.com/ROCm/ATOM/pull/943)** adapts EAGLE 3.1 speculative decoding by adding `fc_norm` and post-norm feedback mechanisms. It also introduces MLA draft support for the Kimi K2.6 model, enhancing speculative decode acceptance rates.

## More changes by area

<details>
<summary>Performance (4)</summary>

- [#1038](https://github.com/ROCm/ATOM/pull/1038) refine PA dispatch for better performance
- [#1047](https://github.com/ROCm/ATOM/pull/1047) enable DeepSeek V3.2 quick reduce envs
- [#1048](https://github.com/ROCm/ATOM/pull/1048) enable DeepSeek V3.2 quick reduce envs
- [#1057](https://github.com/ROCm/ATOM/pull/1057) (newly opened) add preshuffle logic for HIP fused_moe

</details>

<details>
<summary>Kernels & attention (7)</summary>

- [#863](https://github.com/ROCm/ATOM/pull/863) refactor SGL plugin attention
- [#954](https://github.com/ROCm/ATOM/pull/954) separate Gated Delta Net (GDN) logic
- [#1079](https://github.com/ROCm/ATOM/pull/1079) enable index cache feature for DSA model
- [#1051](https://github.com/ROCm/ATOM/pull/1051) refine PA dispatch for minimax
- [#1103](https://github.com/ROCm/ATOM/pull/1103) (newly opened) enable DBO for vLLM plugin
- [#1104](https://github.com/ROCm/ATOM/pull/1104) (newly opened) add 2D-tiled causal_conv1d prefill kernel for gated delta net
- [#1054](https://github.com/ROCm/ATOM/pull/1054) (newly opened) restore missing concat+quant kernel from original vLLM MLA

</details>

<details>
<summary>MoE & quantization (8)</summary>

- [#1027](https://github.com/ROCm/ATOM/pull/1027) support DeepSeek V4 online quantization
- [#963](https://github.com/ROCm/ATOM/pull/963) fuse qknorm and quantization for DeepSeek V2
- [#875](https://github.com/ROCm/ATOM/pull/875) enable Expert Parallelism (EP) for DeepSeek V4
- [#1088](https://github.com/ROCm/ATOM/pull/1088) support DeepSeek V4 DP+EP and fix dump accuracy
- [#1091](https://github.com/ROCm/ATOM/pull/1091) (newly opened) add EP and pad support for Step-3.5-Flash-FP8
- [#1055](https://github.com/ROCm/ATOM/pull/1055) (newly opened) fuse input_rmsnorm_quant and qknorm_quant for DPSK V2
- [#1045](https://github.com/ROCm/ATOM/pull/1045) (newly opened) add Triton MoE A8W4 support for GPT-OSS
- [#1067](https://github.com/ROCm/ATOM/pull/1067) (newly opened) add MoE A8W4 GEMM support for GPT-OSS

</details>

<details>
<summary>Model support (3)</summary>

- [#996](https://github.com/ROCm/ATOM/pull/996) support DeepSeek-V4-Flash-Base on gfx942
- [#1050](https://github.com/ROCm/ATOM/pull/1050) adjust GPU memory utilization to 0.8 for gpt-oss-120b
- [#1126](https://github.com/ROCm/ATOM/pull/1126) (newly opened) add DeepSeek R1 MXFP4 v2 recipe case

</details>

<details>
<summary>Parallelism & scheduling (3)</summary>

- [#869](https://github.com/ROCm/ATOM/pull/869) add ZMQ publisher for KV cache events
- [#1121](https://github.com/ROCm/ATOM/pull/1121) enable TBO compute/comm overlap in DeepSeek V4
- [#1049](https://github.com/ROCm/ATOM/pull/1049) enable dualstream in MTP

</details>

<details>
<summary>API & serving (8)</summary>

- [#549](https://github.com/ROCm/ATOM/pull/549) add RLHF rollout integration support for verl
- [#1006](https://github.com/ROCm/ATOM/pull/1006) upgrade vLLM version to v0.22.0
- [#1085](https://github.com/ROCm/ATOM/pull/1085) add hidden states extraction for TorchSpec training
- [#1080](https://github.com/ROCm/ATOM/pull/1080) enable index cache feature for DSA model
- [#964](https://github.com/ROCm/ATOM/pull/964) support standalone draft model in ATOM SGL
- [#1052](https://github.com/ROCm/ATOM/pull/1052) upgrade SGLang from v0.5.10 to v0.5.12
- [#1129](https://github.com/ROCm/ATOM/pull/1129) (newly opened) format and add TLS for HTTP server
- [#1101](https://github.com/ROCm/ATOM/pull/1101) (newly opened) support DP and EP in vLLM plugin

</details>

<details>
<summary>Hardware & arch (1)</summary>

- [#1031](https://github.com/ROCm/ATOM/pull/1031) use ATOM_USE_FP4_NON_SHUFFLE_TRITON_GEMM for non-shuffle Triton GEMM

</details>

<details>
<summary>Refactors (2)</summary>

- [#1095](https://github.com/ROCm/ATOM/pull/1095) rename atom-mesh to atomesh for brand alignment
- [#1086](https://github.com/ROCm/ATOM/pull/1086) unify engine utility command dispatch into EngineUtilityHandler

</details>

<details>
<summary>Docs (3)</summary>

- [#912](https://github.com/ROCm/ATOM/pull/912) introduce online quantization documentation
- [#1061](https://github.com/ROCm/ATOM/pull/1061) fix misattributed plugin PR citations in v0.1.3 release notes
- [#1063](https://github.com/ROCm/ATOM/pull/1063) add notes to v0.1.3 release notes

</details>

<details>
<summary>Bugfixes (21)</summary>

- [#905](https://github.com/ROCm/ATOM/pull/905) fail fast when page-size is less than KV element width
- [#1076](https://github.com/ROCm/ATOM/pull/1076) fix fused shared+routed MoE accuracy on DeepSeek-V4-Flash-Base
- [#1064](https://github.com/ROCm/ATOM/pull/1064) fix atomesh standalone arguments routing
- [#1109](https://github.com/ROCm/ATOM/pull/1109) fix V4 TBO hang and hash topk single all-gather
- [#1003](https://github.com/ROCm/ATOM/pull/1003) fix sparse_attn_v4_paged_prefill for MI308
- [#1112](https://github.com/ROCm/ATOM/pull/1112) disable prefix cache in linear attention
- [#1032](https://github.com/ROCm/ATOM/pull/1032) fix chunk prefill
- [#1058](https://github.com/ROCm/ATOM/pull/1058) drop redundant cu_seqlens_q refill in attention metadata builder
- [#1072](https://github.com/ROCm/ATOM/pull/1072) fix DP EP failure in ATOM SGLang
- [#1059](https://github.com/ROCm/ATOM/pull/1059) fix V2 model launch issue in ATOM SGL
- [#1087](https://github.com/ROCm/ATOM/pull/1087) fix EP for modular
- [#1046](https://github.com/ROCm/ATOM/pull/1046) fix MTP+DP speculative-num-steps > 1 error
- [#1119](https://github.com/ROCm/ATOM/pull/1119) fix quant config read logic in model loading
- [#1024](https://github.com/ROCm/ATOM/pull/1024) fix warmup using full token budget for DP
- [#1105](https://github.com/ROCm/ATOM/pull/1105) fix DeepSeek V4 indexcache
- [#1132](https://github.com/ROCm/ATOM/pull/1132) fix MoE fallback route
- [#1090](https://github.com/ROCm/ATOM/pull/1090) fix Kimi 2.5 issue
- [#1077](https://github.com/ROCm/ATOM/pull/1077) support DeepSeek-V4-Flash-FP8 on gfx942 device
- [#1100](https://github.com/ROCm/ATOM/pull/1100) remove VLLM_USE_V2_MODEL_RUNNER for 128 concurrency in GPT-OSS
- [#1102](https://github.com/ROCm/ATOM/pull/1102) fix MHC fallback
- [#1128](https://github.com/ROCm/ATOM/pull/1128) (newly opened) fix fused shared expert in Qwen3.5-FP4

</details>

<details>
<summary>CI & build (33)</summary>

- [#1110](https://github.com/ROCm/ATOM/pull/1110) unify catalog matrix and fix ROCm/CI quoting
- [#1093](https://github.com/ROCm/ATOM/pull/1093) remove atom-mesh benchmark and accuracy workflows
- [#1005](https://github.com/ROCm/ATOM/pull/1005) change AW execution logic to one server multi jobs
- [#1124](https://github.com/ROCm/ATOM/pull/1124) (newly opened) add V4 1p1d/2p1d slurm scripts with nightly docker image
- [#1040](https://github.com/ROCm/ATOM/pull/1040) align recipe to nightly script
- plus 28 more minor CI updates (including aiter artifact pins, benchmark matrix splits, and docker image bumps)

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (ATOM.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
