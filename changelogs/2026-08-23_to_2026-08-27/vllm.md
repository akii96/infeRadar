# vllm: PR digest (2026-08-23 to 2026-08-27)

_176 merged, 396 newly opened - source vllm-project/vllm, generated 2026-08-27T19:47:16Z_

## TL;DR
- **DeepSeek** dominated model updates this window (28 PRs), with major additions for DeepSeek-V4 including FlashInfer MoE backends, FP8 quantization, and fused C4 compressor GEMMs.
- **Performance & Kernels** saw massive needle-moving work, notably the introduction of HiSparse for host-resident sparse-MLA decode hot-buffering, and batch-invariant persistent matmul tuning that yields up to 3x decode speedups on RTX 4090D/H20.
- **MoE & Quantization** advanced with Humming support for MXFP4 weights and block-FP8 activations, alongside new FP8 fused_moe tuning for Qwen3.5.
- **Overall direction** points heavily toward extreme scale and disaggregation, evidenced by massive newly-opened work on disk-backed PLE n-gram tables, streaming session APIs, and peer-to-peer RDT weight synchronization for RL workloads.

## Most important PRs
- **[#51323](https://github.com/vllm-project/vllm/pull/51323)** Implements HiSparse, a host-resident sparse-MLA decode hot-buffering system. This significantly improves decode performance for models using sparse MLA by optimizing KV cache and attention metadata handling.
- **[#53247](https://github.com/vllm-project/vllm/pull/53247)** Adds architecture-specific tuned configurations for batch-invariant persistent matmul. This optimization delivers up to 3x faster decode kernels on RTX 4090D and H20 GPUs.
- **[#51332](https://github.com/vllm-project/vllm/pull/51332)** Introduces Humming quantization support for MXFP4 weights and block-FP8 activations in MoE layers. This enables highly efficient expert execution and reduced memory bandwidth on NVIDIA hardware.
- **[#43375](https://github.com/vllm-project/vllm/pull/43375)** Implements peer-to-peer RDT weight synchronization. This enables efficient, distributed weight updates specifically tailored for reinforcement learning workloads.
- **[#54070](https://github.com/vllm-project/vllm/pull/54070)** Proposes disk-backed offloading for PLE n-gram tables (newly opened). This massive feature aims to drastically reduce memory requirements for large-scale speculative decoding and n-gram matching.

## More changes by area

<details>
<summary>Performance (29)</summary>

- [#53540](https://github.com/vllm-project/vllm/pull/53540) "[ROCm][Perf] Fuse SWA q/kv RMSNorm and q FP8 group quant for DeepSeek-V4"
- [#53838](https://github.com/vllm-project/vllm/pull/53838) "[ROCm][DSV4][Perf] Fuse DeepSeek V4 C4 compressor GEMMs"
- [#52388](https://github.com/vllm-project/vllm/pull/52388) "[K3 Perf] Optimize k3 mamba metadata preparation, 6.6~7.6x kernel performance improvement"
- [#53318](https://github.com/vllm-project/vllm/pull/53318) "[Perf] Tune FlashInfer all-reduce selection on SM103"
- [#53464](https://github.com/vllm-project/vllm/pull/53464) "[Pooling] Improve BGE-M3 sync pooling throughput by up to 3.13%"
- [#53649](https://github.com/vllm-project/vllm/pull/53649) "[Perf] Autotune batch invariance triton kernel in blackwell, 33.6% E2E latency reduction"
- [#53878](https://github.com/vllm-project/vllm/pull/53878) "[Perf][GLM5.2] Fuse sparse MLA Q concatenation with head padding"
- [#53942](https://github.com/vllm-project/vllm/pull/53942) "[Kimi K3 Perf] Optimize `eh_proj` linear calculation, 12.9 ~ 25.2% kernel performance improvement"
- [#53606](https://github.com/vllm-project/vllm/pull/53606) "[Perf] Tune FlashInfer all-reduce thresholds for single-node TP8 on SM103"
- [#54036](https://github.com/vllm-project/vllm/pull/54036) "[Perf][PCP][DSpark] Shard context-KV precompute across PCP ranks" (open)
- [#53953](https://github.com/vllm-project/vllm/pull/53953) "[ROCm][Model][AMD][Performance]: Added AITER fusion on top of the existing TRITON fusion path for GLM-5.2-MXFP4 through deepseek_v32" (open)
- [#54030](https://github.com/vllm-project/vllm/pull/54030) "[Perf][PCP] Fuse direct-KV publication fence" (open)
- [#53592](https://github.com/vllm-project/vllm/pull/53592) "[6/N] HiSparse: add DeepSeek V4 support" (open)
- [#53875](https://github.com/vllm-project/vllm/pull/53875) "[Kernel][Perf] Fuse clamped MoE activation and UE8M0 FP8 block quantization" (open)
- [#53562](https://github.com/vllm-project/vllm/pull/53562) "[Perf][GLM-5.2] Reuse Sparse Physical Indices via Attention Metadata with DCP" (open)
- [#53913](https://github.com/vllm-project/vllm/pull/53913) "[CPU][Perf] Add vectorized Sampler Kernel" (open)
- [#53448](https://github.com/vllm-project/vllm/pull/53448) "[ROCm][Perf] Speed up the lightning indexer's score and top-k k…" (open)
- [#53446](https://github.com/vllm-project/vllm/pull/53446) "[Kernel][Perf] Add Hopper (SM90) tuned config for batch-invariant persistent matmul" (open)
- [#53543](https://github.com/vllm-project/vllm/pull/53543) "[Bugfix][Perf][Attention] Enable masked NVFP4 XQA on SM120" (open)
- [#53782](https://github.com/vllm-project/vllm/pull/53782) "[4/N] Expose HiSparse cache metrics" (open)
- [#53918](https://github.com/vllm-project/vllm/pull/53918) "[ROCm][Perf] Enable AITER fuse_qk_norm_rope_kvcache for Gemma4 (head_dim 512 + V-norm)" (open)
- [#53789](https://github.com/vllm-project/vllm/pull/53789) "[ROCm][Perf] Bound the decode paged-MQA-logits sanitize to the top-k read region" (open)
- [#53833](https://github.com/vllm-project/vllm/pull/53833) "[ROCm][Perf] Fuse MiniMax-M3 sparse cache insertion with AITER" (open)
- [#53623](https://github.com/vllm-project/vllm/pull/53623) "[ROCm][Perf] Enable the AITER GDN decode fast path for flat qkvz layouts" (open)
- [#54088](https://github.com/vllm-project/vllm/pull/54088) "[Kimi Perf] Tune hopper low latency gemm kernel, 4%~97% performance improvement" (open)
- [#53874](https://github.com/vllm-project/vllm/pull/53874) "[ROCm][Perf] Fuse GeGLU activation into aiter FP8 group-quant kernel" (open)
- [#53517](https://github.com/vllm-project/vllm/pull/53517) "[Performance] Optimize Dots3 NOTE runtime" (open)
- [#53847](https://github.com/vllm-project/vllm/pull/53847) "[ROCm][Perf][DeepSeek V4] FP8 shared-expert load-time requant for AITER fused MoE on gfx942" (open)
- [#53710](https://github.com/vllm-project/vllm/pull/53710) "[Kernel][Perf] Tune fused_moe FP8 config for Qwen3-VL on L40S (+8% at batch 4-512)" (open)

</details>

<details>
<summary>Kernels & attention (37)</summary>

- [#52980](https://github.com/vllm-project/vllm/pull/52980) "[SM100] Hdim 256 optimized"
- [#52676](https://github.com/vllm-project/vllm/pull/52676) "[Kernel][Perf] Enable fused QK-norm + partial MRoPE + gate for Qwen3.6"
- [#53534](https://github.com/vllm-project/vllm/pull/53534) "[Kimi K3][Kernel] Enable low-latency decode GEMM dispatch on SM100"
- [#53396](https://github.com/vllm-project/vllm/pull/53396) "[Kimi K3][Kernel] Support DS conv-state layout in fused KDA decode kernel"
- [#51040](https://github.com/vllm-project/vllm/pull/51040) "[ROCm][K3] Extend FP8 asm MLA prefill to non-divisor small head counts"
- [#53705](https://github.com/vllm-project/vllm/pull/53705) "[AttentionBackend][HPC-ops] update hpc rope norm to support stride kv cache"
- [#54012](https://github.com/vllm-project/vllm/pull/54012) "[Attention][DCP] Use FlashInfer native CP for MLA decode"
- [#52157](https://github.com/vllm-project/vllm/pull/52157) "[Attention][Spec Decode] Support varlen trtllm-gen decode for adaptive verification"
- [#53326](https://github.com/vllm-project/vllm/pull/53326) "[Bugfix] Resolve B12X modules before Dynamo tracing"
- [#51398](https://github.com/vllm-project/vllm/pull/51398) "[DeepEPv2] Support MXFp8 Activation Scale Dispatch"
- [#53567](https://github.com/vllm-project/vllm/pull/53567) "[7/N][warmup][DSv4] Migrate MoE execution and distributed kernels" (open)
- [#53566](https://github.com/vllm-project/vllm/pull/53566) "[5/N][warmup][DSv4] Migrate NVIDIA CuTeDSL attention kernels" (open)
- [#54038](https://github.com/vllm-project/vllm/pull/54038) "[ROCm][Perf] Kimi-K3 Fused kernels for KDA prefill reland" (open)
- [#53731](https://github.com/vllm-project/vllm/pull/53731) "[ROCm][Kimi-K3] Re-land fused KDA chunk prefill (gfx950) with a safe multi-arch build" (open)
- [#53909](https://github.com/vllm-project/vllm/pull/53909) "[Kernel][Qwen]Add qwen4 fuse op" (open)
- [#53823](https://github.com/vllm-project/vllm/pull/53823) "[ROCm] Add prequantized FP8 attention for Qwen3 Next" (open)
- [#53564](https://github.com/vllm-project/vllm/pull/53564) "[2/N][warmup][DSv4] Migrate sequence and DCP kernels" (open)
- [#53556](https://github.com/vllm-project/vllm/pull/53556) "[Kimi K3][Kernel] Fuse BF16 shared experts into latent MegaMoE tail" (open)
- [#53475](https://github.com/vllm-project/vllm/pull/53475) "[ROCm] Extend fused KDA decode to DSpark spec (num_spec<=2)" (open)
- [#54040](https://github.com/vllm-project/vllm/pull/54040) "[Kernel] Retire the DSv3 router GEMM CUDA kernel" (open)
- [#53645](https://github.com/vllm-project/vllm/pull/53645) "Add FlashInfer fused decode for Qwen GDN on sm120" (open)
- [#53770](https://github.com/vllm-project/vllm/pull/53770) "[WIP] Add FP8-K NVFP4-V KV cache support" (open)
- [#54066](https://github.com/vllm-project/vllm/pull/54066) "[ROCm][Kimi-K3] Fuse MXFP4 quant into KDA decode" (open)
- [#54068](https://github.com/vllm-project/vllm/pull/54068) "[ROCm][Kimi-K3] Fuse MXFP4 quant into MLA gated o_proj" (open)
- [#53785](https://github.com/vllm-project/vllm/pull/53785) "[Attention] Enable dense and masked MHA for GLM-5" (open)
- [#54032](https://github.com/vllm-project/vllm/pull/54032) "[Kernel] Add a FlashInfer SM90 MXFP4 x FP8 fused MoE backend" (open)
- [#53677](https://github.com/vllm-project/vllm/pull/53677) "[kernel]Fused embedding kernel" (open)
- [#53911](https://github.com/vllm-project/vllm/pull/53911) "[Kernel] Fuse DeepEP-v2 decode globalize+align into one launch" (open)
- [#53525](https://github.com/vllm-project/vllm/pull/53525) "[Kimi-K3] Optimize C=1 KDA PDL pipeline" (open)
- [#54015](https://github.com/vllm-project/vllm/pull/54015) "[Kimi-K3] Merge MLA gate into QKV-A projection" (open)
- [#54093](https://github.com/vllm-project/vllm/pull/54093) "Conv1d" (open)
- [#53526](https://github.com/vllm-project/vllm/pull/53526) "[Kimi-K3] Optimize C=1 MLA concat/cache PDL handoff" (open)
- [#53524](https://github.com/vllm-project/vllm/pull/53524) "[Kimi-K3] Optimize C=1 MoE and AttnRes PDL handoffs" (open)
- [#53465](https://github.com/vllm-project/vllm/pull/53465) "[DCP] Add DCP qrep to GLM-5.2 flat model definition" (open)
- [#54063](https://github.com/vllm-project/vllm/pull/54063) "[ROCm] Consume MXFP4 QuantizedActivation in AITER linear" (open)
- [#53793](https://github.com/vllm-project/vllm/pull/53793) "Fuse ReLU2 with static FP8 activation quantization" (open)
- [#53781](https://github.com/vllm-project/vllm/pull/53781) "[3/N] HiSparse: host-resident sparse-MLA decode hot-buffering" (open)

</details>

<details>
<summary>MoE & quantization (18)</summary>

- [#49636](https://github.com/vllm-project/vllm/pull/49636) "[Model][MoE] DeepSeek-V4: add opt-in FlashInfer moe_ep expert backend"
- [#52821](https://github.com/vllm-project/vllm/pull/52821) "[Refactor] Remove dead code quantization 2"
- [#53819](https://github.com/vllm-project/vllm/pull/53819) "[Kernel][Perf] Tune fused_moe FP8 config for Qwen3.5 on L40S (+7%)"
- [#53101](https://github.com/vllm-project/vllm/pull/53101) "[Model] Add FP8 quantization support for ModernBERT"
- [#53310](https://github.com/vllm-project/vllm/pull/53310) "[Kimi K3 Refactor] Add `UnfinalizedMoEOutput` proto following up for #53152"
- [#53869](https://github.com/vllm-project/vllm/pull/53869) "Bugfix: use PCP slot mappings for PIECEWISE capture"
- [#53311](https://github.com/vllm-project/vllm/pull/53311) "[MoE] enable all2all fi_one_sided by default"
- [#54056](https://github.com/vllm-project/vllm/pull/54056) "Fix Humming MoE activation_output aliasing"
- [#53805](https://github.com/vllm-project/vllm/pull/53805) "[Revert] MXFP4 + block-FP8 Humming support after H100 correctness failure" (open)
- [#54024](https://github.com/vllm-project/vllm/pull/54024) "[CPU][Zen] Add DA8W4 (W4A8) int4 support for dense and MoE layers" (open)
- [#53848](https://github.com/vllm-project/vllm/pull/53848) "[Model][Quantization] Support GLM W4AFP8 checkpoints with Humming" (open)
- [#53897](https://github.com/vllm-project/vllm/pull/53897) "[MoE] Support out-of-tree fp8 MoE backends" (open)
- [#53527](https://github.com/vllm-project/vllm/pull/53527) "[DSV4][SM90] add dsv4 fp8 weight use mega_moe backend" (open)
- [#53741](https://github.com/vllm-project/vllm/pull/53741) "[ModelOpt] Support fused MoE weight reload" (open)
- [#53585](https://github.com/vllm-project/vllm/pull/53585) "[Cleanup] Remove online quantization support in `fp8.py` in favor of online shorthands" (open)
- [#54006](https://github.com/vllm-project/vllm/pull/54006) "[Quantization][Autoround][XPU] Add MXFP4 Hadamard rotation support" (open)
- [#53709](https://github.com/vllm-project/vllm/pull/53709) "[Model][Quant] DeepSeek-V4: opt-in lossless MXFP4->block-FP8 expert dequant (Hopper prefill speedup)" (open)
- [#53880](https://github.com/vllm-project/vllm/pull/53880) "[Quantization] Support Humming W4A8 Block in CT" (open)

</details>

<details>
<summary>Model support (35)</summary>

- [#53608](https://github.com/vllm-project/vllm/pull/53608) "[Model] Remove ten deprecated model architectures"
- [#53615](https://github.com/vllm-project/vllm/pull/53615) "[Model] Migrate FlexOlmo, Olmo3 and Hunyuan V1/VL to the Transformers modeling backend"
- [#52185](https://github.com/vllm-project/vllm/pull/52185) "[Model] Pixtral: use packed multimodal encoder attention"
- [#52874](https://github.com/vllm-project/vllm/pull/52874) "[Bugfix][Model] Mistral3: fix image placeholder grid for processor size overrides"
- [#51262](https://github.com/vllm-project/vllm/pull/51262) "[Bugfix][DeepSeek V4] Handle trailing system messages in prompt rendering"
- [#53830](https://github.com/vllm-project/vllm/pull/53830) "[Bugfix][Model] Honor Molmo2 dummy video num_frames >= 2 override"
- [#53456](https://github.com/vllm-project/vllm/pull/53456) "[Bugfix] Keep grid dims for XD-RoPE models on a prefix-cache hit"
- [#51302](https://github.com/vllm-project/vllm/pull/51302) "[Bugfix][Model] deepseek-vl2: restore original DeepseekV2Config defaults for omitted language_config fields"
- [#53697](https://github.com/vllm-project/vllm/pull/53697) "[Model] Remove unused DeepSeek V4 top-k buffer helper"
- [#53884](https://github.com/vllm-project/vllm/pull/53884) "[Bugfix] Make Gemma4 MTP suppress_tokens masking CUDA-graph-safe"
- [#50536](https://github.com/vllm-project/vllm/pull/50536) "fix(config): guard LlamaBidirectionalConfig against missing hf_config.pooling"
- [#53899](https://github.com/vllm-project/vllm/pull/53899) "Support PLE-Offload for Qwen3.8-Flash-Next" (open)
- [#53896](https://github.com/vllm-project/vllm/pull/53896) "[Model] Support Qwen3.8-Flash-Next" (open)
- [#53906](https://github.com/vllm-project/vllm/pull/53906) "[Model] add GLM-5.3-Flash support" (open)
- [#53438](https://github.com/vllm-project/vllm/pull/53438) "[Reload] Add manifest-driven streaming modelwise weight reload" (open)
- [#53806](https://github.com/vllm-project/vllm/pull/53806) "Add K2-Horizon model support" (open)
- [#53811](https://github.com/vllm-project/vllm/pull/53811) "[Model] Remove native LongCat implementations" (open)
- [#54051](https://github.com/vllm-project/vllm/pull/54051) "[WIP][Model] Add upcoming XingChen4 model support" (open)
- [#53964](https://github.com/vllm-project/vllm/pull/53964) "[Feature] Add request-static YaRN profiles for mRoPE" (open)
- [#53599](https://github.com/vllm-project/vllm/pull/53599) "[Model] Optimize kimi_k25_vit" (open)
- [#53165](https://github.com/vllm-project/vllm/pull/53165) "[Bugfix][Multimodal] Encode text in mixed CLIP/SigLIP pooling batches"
- [#53553](https://github.com/vllm-project/vllm/pull/53553) "[Bugfix][MM] Fix JinaVL processing cache order"
- [#53560](https://github.com/vllm-project/vllm/pull/53560) "[MM] Cache common token sequences"
- [#53656](https://github.com/vllm-project/vllm/pull/53656) "[Config][EC] Normalize producer-only encoder config"
- [#53854](https://github.com/vllm-project/vllm/pull/53854) "[Bugfix][Processor] Replace bare asserts with ValueError in DeepseekVLV2/OCR processors"
- [#52786](https://github.com/vllm-project/vllm/pull/52786) "[LoRA] Add Qwen3-Omni multimodal LoRA support"
- [#53361](https://github.com/vllm-project/vllm/pull/53361) "[LoRA] feat: Support LoRA for DeepSeek V4"
- [#53843](https://github.com/vllm-project/vllm/pull/53843) "[LoRA] Cleanup VocabParallelEmbedding"
- [#51157](https://github.com/vllm-project/vllm/pull/51157) "[Bugfix][Frontend] Let pooling requests set padding"
- [#53513](https://github.com/vllm-project/vllm/pull/53513) "[Bugfix][LoRA] Add multimodal module mapping for Muse-Glimmer"
- [#53519](https://github.com/vllm-project/vllm/pull/53519) "[Bugfix][LoRA] Restore tower and connector LoRA support for LFM2-VL"
- [#53557](https://github.com/vllm-project/vllm/pull/53557) "[Bugfix][LoRA] Enable tower/connector LoRA for Qwen3-Omni"
- [#53610](https://github.com/vllm-project/vllm/pull/53610) "[MM] Further cleanup _apply_hf_processor_main" (open)
- [#53849](https://github.com/vllm-project/vllm/pull/53849) "[Feature][LoRA] Support per-module MM mappings for Granite Speech" (open)
- [#53809](https://github.com/vllm-project/vllm/pull/53809) "[MM] Add a Mooncake-store backend for the multi-modal processor cache" (open)
- [#53675](https://github.com/vllm-project/vllm/pull/53675) "[Multimodal] Use GPU NVDEC for EPD encoder-only instance video media IO" (open)
- [#53555](https://github.com/vllm-project/vllm/pull/53555) "[LoRA] Support modules_to_save for sequence classification" (open)

</details>

<details>
<summary>Parallelism & scheduling (49)</summary>

- [#49994](https://github.com/vllm-project/vllm/pull/49994) "[EC Connector] EC Offloading Connector use events instead of StepTracker"
- [#53751](https://github.com/vllm-project/vllm/pull/53751) "[RL] Support checkpoint-coordinate sparse NCCL weight updates"
- [#53265](https://github.com/vllm-project/vllm/pull/53265) "[3/N][KV Connector][NIXL] Support per-region transfer geometry"
- [#51335](https://github.com/vllm-project/vllm/pull/51335) "[5/N] Expose HiSparse cache metrics"
- [#53779](https://github.com/vllm-project/vllm/pull/53779) "[1/N][KV Connector] Identify externally transferable KV cache groups"
- [#53698](https://github.com/vllm-project/vllm/pull/53698) "[Bugfix][ROCm][Disagg] Fix MoRIIO shared KV memory region registration"
- [#53354](https://github.com/vllm-project/vllm/pull/53354) "[NIXL] Simplify host-stager progress and shutdown"
- [#52497](https://github.com/vllm-project/vllm/pull/52497) "[RL] Add rank-local IPC weight updates"
- [#52914](https://github.com/vllm-project/vllm/pull/52914) "[Bugfix][DP] Synchronize the device on pause completion"
- [#53523](https://github.com/vllm-project/vllm/pull/53523) "[Bugfix][NIXL] Fix Mamba prefill truncation ordering"
- [#53663](https://github.com/vllm-project/vllm/pull/53663) "[Bugfix][Mooncake] Fix Mamba prefill truncation ordering"
- [#52951](https://github.com/vllm-project/vllm/pull/52951) "[Bugfix] Reuse CUDA streams in packed weight transfer to cap reserved-memory waste"
- [#53952](https://github.com/vllm-project/vllm/pull/53952) "[Bugfix] Restore portable all2all backend default"
- [#51292](https://github.com/vllm-project/vllm/pull/51292) "[Core] Disable fuse_allreduce_rms under VLLM_BATCH_INVARIANT (non-deterministic under TP)"
- [#53378](https://github.com/vllm-project/vllm/pull/53378) "[Elastic EP] Preserve AOT cache reuse during scaling"
- [#53730](https://github.com/vllm-project/vllm/pull/53730) "[DCP][Mooncake] Harden hybrid prefix-cache external hits" (open)
- [#53422](https://github.com/vllm-project/vllm/pull/53422) "[Feature] Add PCP O-Proj tensor parallelism" (open)
- [#53624](https://github.com/vllm-project/vllm/pull/53624) "[KV Offload] Add KVCR secondary-tier adapter" (open)
- [#53571](https://github.com/vllm-project/vllm/pull/53571) "[feat]Add SLO-aware scheduling policy" (open)
- [#53784](https://github.com/vllm-project/vllm/pull/53784) "[Distributed] Support pre-shared ncclUniqueId rendezvous for weight transfer" (open)
- [#53780](https://github.com/vllm-project/vllm/pull/53780) "[2/N][KV Connector][NIXL] Support per-region transfer geometry" (open)
- [#53948](https://github.com/vllm-project/vllm/pull/53948) "[MRV2][PP] Prototype deferred sampled-result receives" (open)
- [#53902](https://github.com/vllm-project/vllm/pull/53902) "[Metrics][KV Offload] Add vllm:kv_offload_cpu_config_info for tier capacity" (open)
- [#53576](https://github.com/vllm-project/vllm/pull/53576) "[Distributed] Add opt-in FlashInfer PCIe IPC all-reduce backend" (open)
- [#53721](https://github.com/vllm-project/vllm/pull/53721) "[ROCm][Connector]: SWA+HMA-support in MoRI-IO connector (Gemma4)" (open)
- [#53825](https://github.com/vllm-project/vllm/pull/53825) "[KV Connector][Mooncake] Send disaggregated KV as whole pages when la…" (open)
- [#54033](https://github.com/vllm-project/vllm/pull/54033) "[Refactor][EC Connector] Add backend extension points to ECCPUWorker" (open)
- [#53664](https://github.com/vllm-project/vllm/pull/53664) "Add pipeline_parallel support for the kimik3 model" (open)
- [#53453](https://github.com/vllm-project/vllm/pull/53453) "[KVConnector][P2P] Configurable unbound-store timeout and one-RTT rejection of a late fetch" (open)
- [#52783](https://github.com/vllm-project/vllm/pull/52783) "[Spec Decode] Enable adaptive DSpark on SM100 sparse MLA"
- [#53694](https://github.com/vllm-project/vllm/pull/53694) "[Model Runner V2][Spec Decode] Skip DP sync before EAGLE/MTP draft prefill"
- [#53435](https://github.com/vllm-project/vllm/pull/53435) "Dflash2 load fix"
- [#53336](https://github.com/vllm-project/vllm/pull/53336) "[Bugfix][Spec Decode] Reapply group geometry for FlashAttention metadata"
- [#52242](https://github.com/vllm-project/vllm/pull/52242) "[Feature][DSpark]: Logprobs adaptive verification"
- [#52193](https://github.com/vllm-project/vllm/pull/52193) "speculative decoding under tensor parallelism (TP>1) , workspace creation select max hidden dim of target and draft model"
- [#53962](https://github.com/vllm-project/vllm/pull/53962) "[Bugfix][Scheduler] Don't pad spec decode up to `max_model_len`"
- [#53121](https://github.com/vllm-project/vllm/pull/53121) "Add MTP support for Nemotron VL models"
- [#53753](https://github.com/vllm-project/vllm/pull/53753) "[Model][Spec Decode] Orthrus diffusion-mode decoding (WIP)" (open)
- [#53979](https://github.com/vllm-project/vllm/pull/53979) "[Attention][Spec Decode] NVFP4 KV: open the FA2 non-causal prefill wrapper for DFlash-family drafters (sm12x)" (open)
- [#53929](https://github.com/vllm-project/vllm/pull/53929) "[Spec Decode] Enable adaptive DSpark verification for Qwen GDN" (open)
- [#53901](https://github.com/vllm-project/vllm/pull/53901) "[ROCm][Spec Decode] Enable Kimi-K3 DSpark with pipeline parallelism" (open)
- [#53720](https://github.com/vllm-project/vllm/pull/53720) "[Spec Decode] Support Qwen3-VL DSpARK" (open)
- [#53630](https://github.com/vllm-project/vllm/pull/53630) "[Spec Decode] Verify in head dtype and drop the FP32 chunk workaround" (open)
- [#53577](https://github.com/vllm-project/vllm/pull/53577) "[DSpark] Support pipeline-parallel prefill in disaggregated serving (+ padded graph batch safety)" (open)
- [#53426](https://github.com/vllm-project/vllm/pull/53426) "[Core][Spec Decode] Opt-in skip of the K=0 draft sync forward (MTP + DFlash, default off)" (open)
- [#53653](https://github.com/vllm-project/vllm/pull/53653) "[Spec Decode] Support PCP-sharded MTP prefill" (open)
- [#53987](https://github.com/vllm-project/vllm/pull/53987) "[Spec Decode][ROCm] Add FLy: entropy-gated deferred verification for draft-model speculative decoding" (open)
- [#53427](https://github.com/vllm-project/vllm/pull/53427) "feat(PCP)(Spec Decode): Support MTP and DSpark with PCP" (open)
- [#53661](https://github.com/vllm-project/vllm/pull/53661) "[PCP][Spec Decode] Support MTP speculative decoding with PCP" (open)
- [#53827](https://github.com/vllm-project/vllm/pull/53827) "[Spec Decode] Add bounded attention for Llama EAGLE3 drafts" (open)

</details>

<details>
<summary>Hardware & arch (24)</summary>

- [#50465](https://github.com/vllm-project/vllm/pull/50465) "[Model Runner V2] batch-sharded sample"
- [#53306](https://github.com/vllm-project/vllm/pull/53306) "[Model Runner V2] Reserve CUDA graph memory"
- [#53407](https://github.com/vllm-project/vllm/pull/53407) "[Bugfix][MRV2] Dispatch uniform decode to a padded FULL cudagraph"
- [#53183](https://github.com/vllm-project/vllm/pull/53183) "[Model Runner V2] Use MRV2 for all models by default"
- [#53515](https://github.com/vllm-project/vllm/pull/53515) "BugFix(PCP): use persistent input buffers for PIECEWISE CUDA graphs"
- [#53682](https://github.com/vllm-project/vllm/pull/53682) "[Bugfix][MRV2] Run cudagraph memory profiling in a throwaway graph pool"
- [#53955](https://github.com/vllm-project/vllm/pull/53955) "[Bugfix] Release CUDA graph profiling memory before KV cache allocation"
- [#53581](https://github.com/vllm-project/vllm/pull/53581) "[Bugfix][Kimi K3] Skip absent metadata during CUDA graph profiling"
- [#53818](https://github.com/vllm-project/vllm/pull/53818) "[Bugfix][ROCm] Capture CUDA graphs on the current stream"
- [#53593](https://github.com/vllm-project/vllm/pull/53593) "[Bugfix] BailingMoeV3 KDA: skip absent metadata during CUDA graph profiling"
- [#53773](https://github.com/vllm-project/vllm/pull/53773) "[Kimi Bug] Fix k3 torch.AcceleratorError: CUDA error: an illegal memory access was encountered"
- [#53853](https://github.com/vllm-project/vllm/pull/53853) "[Config] Delegate PCP compatibility checks to PCP manager"
- [#53558](https://github.com/vllm-project/vllm/pull/53558) "[Core][Feat] Pluggable KVCacheConfigBuilder for platform/model-specific KV cache planning" (open)
- [#53614](https://github.com/vllm-project/vllm/pull/53614) "[Kimi K3] Support internal prefix checkpoints with partial prefix caching and spec-decoding" (open)
- [#53598](https://github.com/vllm-project/vllm/pull/53598) "[ROCm][DSpark][DCP] Serve prefix cache hits under DCP for Kimi-K3" (open)
- [#53867](https://github.com/vllm-project/vllm/pull/53867) "[Feature][PCP] Support decode-only FULL CUDA graphs" (open)
- [#53871](https://github.com/vllm-project/vllm/pull/53871) "[Core] KV cache: block-range eviction for live requests" (open)
- [#53904](https://github.com/vllm-project/vllm/pull/53904) "[Core][V1] Reuse request token storage for trace replay" (open)
- [#53491](https://github.com/vllm-project/vllm/pull/53491) "[Core] Enhance cpu<->gpu sync checking to include paged async copies" (open)
- [#54061](https://github.com/vllm-project/vllm/pull/54061) "[Profiler] Extend CUDA graph capture profiling to the V2 model runner" (open)
- [#53895](https://github.com/vllm-project/vllm/pull/53895) "[MRV2] Add platform-provided runner component factory" (open)
- [#53639](https://github.com/vllm-project/vllm/pull/53639) "[WIP][PCP] Dispatch CUDA graphs by rank-local token count" (open)
- [#53997](https://github.com/vllm-project/vllm/pull/53997) "[XPU][V2] Keep grammar-bitmask copies on the current stream under XPU graphs" (open)
- [#53450](https://github.com/vllm-project/vllm/pull/53450) "[Platform] Allow pinning the attention backend for components that auto-select" (open)

</details>

<details>
<summary>API & serving (45)</summary>

- [#53500](https://github.com/vllm-project/vllm/pull/53500) "[Frontend] Move run_batch.py out openai folder"
- [#53372](https://github.com/vllm-project/vllm/pull/53372) "[MM] Simplify prompt updates: replace `PromptSeq` with `list[int]`"
- [#51896](https://github.com/vllm-project/vllm/pull/51896) "Reject oversized media before fully downloading it"
- [#52840](https://github.com/vllm-project/vllm/pull/52840) "[Rust Frontend][gRPC] Add LoRA lifecycle control"
- [#53218](https://github.com/vllm-project/vllm/pull/53218) "[Rust Frontend] Align OpenAI request and response edge cases"
- [#53219](https://github.com/vllm-project/vllm/pull/53219) "Add Cohere ChatV2 render endpoint"
- [#51034](https://github.com/vllm-project/vllm/pull/51034) "feat: add SSE keep-alive comments for idle streaming responses"
- [#52209](https://github.com/vllm-project/vllm/pull/52209) "Add routed expert loading for gpt-oss"
- [#52764](https://github.com/vllm-project/vllm/pull/52764) "[warmup] overlap renderer warmup and engine core initialization"
- [#45803](https://github.com/vllm-project/vllm/pull/45803) "[Frontend] Add `/v1/messages/render` endpoint for the Anthropic Messages API"
- [#48922](https://github.com/vllm-project/vllm/pull/48922) "[Bugfix] Guard tool call argument JSON parsing in chat message postprocessing"
- [#51979](https://github.com/vllm-project/vllm/pull/51979) "[Bugfix] Release worker RPC payload before next dequeue"
- [#53659](https://github.com/vllm-project/vllm/pull/53659) "[Frontend] Move cli_args.py and dp_supervisor.py out openai folder"
- [#53432](https://github.com/vllm-project/vllm/pull/53432) "[Misc] Use VLLMValidationError in offline inference input validation"
- [#50588](https://github.com/vllm-project/vllm/pull/50588) "[Bugfix][Frontend] Fix run_batch upload retrying on success and unawaited error body"
- [#53738](https://github.com/vllm-project/vllm/pull/53738) "[Bugfix][Frontend] Keep credentials out of the Rust frontend launch log"
- [#53965](https://github.com/vllm-project/vllm/pull/53965) "[Bugfix] Preserve parallel HY-V3 calls delivered in one streaming delta"
- [#52467](https://github.com/vllm-project/vllm/pull/52467) "[Misc] Use VLLMValidationError in Cohere request validation"
- [#53999](https://github.com/vllm-project/vllm/pull/53999) "[Bugfix] Raise clear error on interleaved multimodal placeholder overcount"
- [#53625](https://github.com/vllm-project/vllm/pull/53625) "[Bugfix][Frontend] Redact hf_token in the non-default args log"
- [#53750](https://github.com/vllm-project/vllm/pull/53750) "[Bugfix][Frontend] Apply the stop string limit to Cohere requests"
- [#53467](https://github.com/vllm-project/vllm/pull/53467) "[Pooling UX] Improve serve --task error guidance"
- [#53204](https://github.com/vllm-project/vllm/pull/53204) "[Rust Frontend][RL]: report engine world size over gRPC"
- [#53744](https://github.com/vllm-project/vllm/pull/53744) "[Bugfix][Multimodal] Reject malformed base64 audio with 400 instead of 500"
- [#53763](https://github.com/vllm-project/vllm/pull/53763) "[Bugfix] Handle malformed namespace tools"
- [#42644](https://github.com/vllm-project/vllm/pull/42644) "[Bugfix] Thread kv_transfer_params into engine for /inference/v1/generate (disagg)"
- [#50431](https://github.com/vllm-project/vllm/pull/50431) "[sleep functionality] code refactor about sleep/wake_up"
- [#47815](https://github.com/vllm-project/vllm/pull/47815) "[Bugfix][OpenAI] Fix streamed completion logprob offsets with echo"
- [#53879](https://github.com/vllm-project/vllm/pull/53879) "[Frontend] Streaming session API (/v1/streaming)" (open)
- [#53876](https://github.com/vllm-project/vllm/pull/53876) "[Core] Bounded-memory streaming sessions: retention, in-place KV eviction, consolidation" (open)
- [#53419](https://github.com/vllm-project/vllm/pull/53419) "[Rust Frontend] /derender: streaming derender + two-process e2e test (phase 3/3)" (open)
- [#53418](https://github.com/vllm-project/vllm/pull/53418) "[Rust Frontend] /derender: reasoning and tool-call parsing (phase 2/3)" (open)
- [#53454](https://github.com/vllm-project/vllm/pull/53454) "[Rust Frontend] Harden resumable session lifecycle in engine-core-client" (open)
- [#54053](https://github.com/vllm-project/vllm/pull/54053) "[feature] Watermarked generation and detection (Gumbel-max algorithm)" (open)
- [#54064](https://github.com/vllm-project/vllm/pull/54064) "[Responses] Implement usage tracking, streaming final items, incomplete_reason, and MCP/builtin tool rendering" (open)
- [#53936](https://github.com/vllm-project/vllm/pull/53936) "[Core] Make parallel sampling (n>1) reqs admission atomic" (open)
- [#53736](https://github.com/vllm-project/vllm/pull/53736) "[Rust Frontend] Add /v1/embeddings support" (open)
- [#53795](https://github.com/vllm-project/vllm/pull/53795) "[Core][Frontend] Add per-request prefix cache telemetry" (open)
- [#53512](https://github.com/vllm-project/vllm/pull/53512) "[Frontend] Optional post-generation hook on EndpointPlugin" (open)
- [#53733](https://github.com/vllm-project/vllm/pull/53733) "Add streaming prompt prefill support" (open)
- [#53550](https://github.com/vllm-project/vllm/pull/53550) "[Metrics] Add opt-in phase-aware engine iteration histograms" (open)
- [#53756](https://github.com/vllm-project/vllm/pull/53756) "[Rust Frontend][gRPC] Enforce LoRA path validation across transports" (open)
- [#53423](https://github.com/vllm-project/vllm/pull/53423) "[Feature] Add first-class KV hints request envelope for programmatic KV management" (open)
- [#53857](https://github.com/vllm-project/vllm/pull/53857) "[Rust Frontend] Add ling3 tool and reasoning parser support" (open)
- [#53760](https://github.com/vllm-project/vllm/pull/53760) "[Rust Frontend][gRPC] Add audio and video media inputs" (open)
- [#53723](https://github.com/vllm-project/vllm/pull/53723) "[Core] Add default-off preemption_victim="lcf" (least-computed-first) victim policy" (open)
- [#53851](https://github.com/vllm-project/vllm/pull/53851) "[Log][Core] Clarify shm_broadcast long-wait diagnostics" (open)

</details>

<details>
<summary>Bugfixes (75)</summary>

- [#53460](https://github.com/vllm-project/vllm/pull/53460) "[Model] Fix KV cache layout and optimize Dots3 NOTE Omni encoders"
- [#53616](https://github.com/vllm-project/vllm/pull/53616) "[Mypy Fix] Mypy fix for "vllm/model_executor/models/[gG]""
- [#53000](https://github.com/vllm-project/vllm/pull/53000) "Fix MNNVL Lamport mailbox publication and cleanup"
- [#52222](https://github.com/vllm-project/vllm/pull/52222) "[Bugfix][GPT-OSS] Fix strict tool-call grammar to accept Harmony renders"
- [#53329](https://github.com/vllm-project/vllm/pull/53329) "[Bugfix][KV Offload] Defer request-level cascade of in-flight primary keys"
- [#53120](https://github.com/vllm-project/vllm/pull/53120) "[Offloader] Offload submodules that make_layers never reaches"
- [#51031](https://github.com/vllm-project/vllm/pull/51031) "[Bugfix][Kernel] Handle kernel block sizes in V2 DCP slot mapping"
- [#52830](https://github.com/vllm-project/vllm/pull/52830) "[Bugfix][Structured Output] Preserve reasoning adapters for shared parser engines"
- [#52377](https://github.com/vllm-project/vllm/pull/52377) "[Bugfix][DCP] Handle sparse MLA metadata after DCP Manager refactor"
- [#53704](https://github.com/vllm-project/vllm/pull/53704) "[Bugfix] Handle empty FlatLogprobs slices and delta output"
- [#53939](https://github.com/vllm-project/vllm/pull/53939) "[Bugfix][Rust Frontend] Fix LogprobsTensors wire schema mismatch"
- [#53747](https://github.com/vllm-project/vllm/pull/53747) "[Bugfix][Tokenizer] Replace bare asserts in the DeepSeek V4 encoder"
- [#54021](https://github.com/vllm-project/vllm/pull/54021) "[Bugfix][KV Offload] Handle padded GPU cache storage"
- [#51839](https://github.com/vllm-project/vllm/pull/51839) "[Profiler] Fix start_profile permanently no-op after max_iterations auto-stop"
- [#53561](https://github.com/vllm-project/vllm/pull/53561) "fix(security): enforce VLLM_MAX_AUDIO_CLIP_FILESIZE_MB on all audio paths"
- [#53766](https://github.com/vllm-project/vllm/pull/53766) "[CI Bug] Fix kimi test `AssertionError: Aligned Mamba state indices must be precomputed`"
- [#53466](https://github.com/vllm-project/vllm/pull/53466) "[Mypy Fix] Mypy fix for "vllm/model_executor/models/[tT]""
- [#52066](https://github.com/vllm-project/vllm/pull/52066) "[XPU] Fix sparse-MLA metadata sync"
- [#53641](https://github.com/vllm-project/vllm/pull/53641) "[AMD][BugFix] Add gpu_sync_allowed to ROCm AITER FA backend"
- [#53604](https://github.com/vllm-project/vllm/pull/53604) "[Docs] Fix docstring continuation indentation in `routed_experts.py`"
- [#53657](https://github.com/vllm-project/vllm/pull/53657) "[Bugfix] Handle parenthesized Gemma4 tool calls"
- [#52389](https://github.com/vllm-project/vllm/pull/52389) "[Bugfix][XPU] Skip oneCCL warm-up all_reduce when world_size == 1"
- [#53755](https://github.com/vllm-project/vllm/pull/53755) "[Bugfix] Update FlashMLA for sparse decode workspace fix"
- [#53947](https://github.com/vllm-project/vllm/pull/53947) "[Bugfix][Elastic EP] Release a prepared reconfiguration when scaling fails" (open)
- [#53479](https://github.com/vllm-project/vllm/pull/53479) "[Bugfix][V1] Mamba align: materialize a state at every boundary and drop the speculative one-block back-off" (open)
- [#53696](https://github.com/vllm-project/vllm/pull/53696) "[Bugfix][Models] Fix OpenPangu sleep mode with static sinks" (open)
- [#53945](https://github.com/vllm-project/vllm/pull/53945) "[Bugfix][Spec Decode] Cache the Mamba state at the block-grid position of EAGLE resume" (open)
- [#53917](https://github.com/vllm-project/vllm/pull/53917) "[Bugfix][DCP] Handle hybrid cache geometry in offload recovery" (open)
- [#53861](https://github.com/vllm-project/vllm/pull/53861) "[Bugfix] Harden streaming-input session lifecycle" (open)
- [#53803](https://github.com/vllm-project/vllm/pull/53803) "Fix mamba align retention checkpoints" (open)
- [#53507](https://github.com/vllm-project/vllm/pull/53507) "[Bugfix][Models] Register sleep-managed runtime buffers" (open)
- [#53508](https://github.com/vllm-project/vllm/pull/53508) "[Bugfix][MRV2] Isolate sleep-mode KV allocations" (open)
- [#53728](https://github.com/vllm-project/vllm/pull/53728) "fix(sample): keep grammar authoritative when min_tokens would empty the mask" (open)
- [#54023](https://github.com/vllm-project/vllm/pull/54023) "[Bugfix] Revert renderer warmup overlap to avoid fork deadlock" (open)
- [#54079](https://github.com/vllm-project/vllm/pull/54079) "[Mypy Fix] Mypy fix for model H/I" (open)
- [#53605](https://github.com/vllm-project/vllm/pull/53605) "fix(warmup): cover all C128A extra_topk widths in sparse-MLA autotune" (open)
- [#53765](https://github.com/vllm-project/vllm/pull/53765) "fix(parser): enforce required tool choice with gemma4 tool parser" (open)
- [#53496](https://github.com/vllm-project/vllm/pull/53496) "[Bugfix][KVConnector] Key ExampleConnector storage on block hashes" (open)
- [#54090](https://github.com/vllm-project/vllm/pull/54090) "[Bugfix] Add compilation timeout for JSON schema and grammar in xgrammar" (open)
- [#53532](https://github.com/vllm-project/vllm/pull/53532) "[Bugfix][KV Offloading] Fix eager SimpleCPUOffload cache registration and final flush" (open)
- [#53511](https://github.com/vllm-project/vllm/pull/53511) "[Bugfix][MiniMax] Reset Lamport workspace after wake-up" (open)
- [#53693](https://github.com/vllm-project/vllm/pull/53693) "[Bugfix][Performance] Restore WNA16 CUDA dispatch and trim MoE workspace" (open)
- [#53473](https://github.com/vllm-project/vllm/pull/53473) "fix(security): enforce prompt-count bound on pooling and scoring routes" (open)
- [#54077](https://github.com/vllm-project/vllm/pull/54077) "[Bugfix][Spec Decode] Profile adaptive verification tails as mixed batches" (open)
- [#53724](https://github.com/vllm-project/vllm/pull/53724) "Fix compressed tensors MXFP4 MoE backend" (open)
- [#53647](https://github.com/vllm-project/vllm/pull/53647) "[Bugfix] Make speculative-decode logprob test tie-aware" (open)
- [#53662](https://github.com/vllm-project/vllm/pull/53662) "Fix DFlash2 draft model initialization" (open)
- [#53686](https://github.com/vllm-project/vllm/pull/53686) "Revert CRCR nightly reporter until execution ordering is fixed" (open)
- [#53510](https://github.com/vllm-project/vllm/pull/53510) "[Bugfix][Humming] Recover locks after sleep and reload" (open)
- [#54076](https://github.com/vllm-project/vllm/pull/54076) "[Bugfix][V1] Use the Mamba cache group's block size for align-mode chunk splitting" (open)
- [#54065](https://github.com/vllm-project/vllm/pull/54065) "[Bugfix][Spec Decode] Profile adaptive verification tail on a schedulable batch shape" (open)
- [#53768](https://github.com/vllm-project/vllm/pull/53768) "[Bugfix][Tokenizer] Handle trailing system messages in DeepSeek V3.2 rendering" (open)
- [#53842](https://github.com/vllm-project/vllm/pull/53842) "[Bugfix][MRV2][LoRA] Fix prompt logprobs mapping" (open)
- [#53774](https://github.com/vllm-project/vllm/pull/53774) "[Revert] Restore per-group K3 Mamba metadata preparation" (open)
- [#53826](https://github.com/vllm-project/vllm/pull/53826) "[Bugfix][Model Runner V2] Preserve sampling masks in batch-sharded sampling" (open)
- [#54042](https://github.com/vllm-project/vllm/pull/54042) "[Bugfix][CPU] Fix several bugs" (open)
- [#53652](https://github.com/vllm-project/vllm/pull/53652) "[Bugfix] Honor default_proposal_method when selecting the speculators proposal method" (open)
- [#53440](https://github.com/vllm-project/vllm/pull/53440) "[Bugfix] Replace non-deterministic index_add_ with scatter-then-sum in TopKWeightAndReduceNaiveBatched" (open)
- [#53499](https://github.com/vllm-project/vllm/pull/53499) "[Bugfix] Scale block size before padding a unified KV page" (open)
- [#53808](https://github.com/vllm-project/vllm/pull/53808) "[Bugfix][Multimodal] Honor modality-scoped mm_processor_kwargs" (open)
- [#53490](https://github.com/vllm-project/vllm/pull/53490) "[Benchmark] Fix MoE tuner cache cleanup and OOM recovery" (open)
- [#53967](https://github.com/vllm-project/vllm/pull/53967) "[Bugfix][Model] Detect FP8_DYNAMIC quantization from llmcompressor recipe.yaml" (open)
- [#53681](https://github.com/vllm-project/vllm/pull/53681) "[Bugfix][Kernel] NVFP4 KV cache: fix block_size/layout detection for physically shaped HND caches" (open)
- [#53570](https://github.com/vllm-project/vllm/pull/53570) "[Bugfix] Support NVIDIA short-form UUID in CUDA_VISIBLE_DEVICES (#51677)" (open)
- [#53628](https://github.com/vllm-project/vllm/pull/53628) "[BugFix][ROCM] DFlash2 fix sliding-window prefix attention NaNs" (open)
- [#54014](https://github.com/vllm-project/vllm/pull/54014) "[Bugfix][KV Offload] Check cgroup memory before SHM allocation" (open)
- [#53603](https://github.com/vllm-project/vllm/pull/53603) "[MRv2][Bugfix] Initialize DCP metadata" (open)
- [#54022](https://github.com/vllm-project/vllm/pull/54022) "[Bugfix] Gracefully handle unsupported reasoning_effort in chat templates" (open)
- [#54026](https://github.com/vllm-project/vllm/pull/54026) "[Bugfix] Return validation errors for malformed OpenAI request fields" (open)
- [#54089](https://github.com/vllm-project/vllm/pull/54089) "[Bugfix][Parser] Scope reasoning-end detection to the current turn via turn-boundary tokens" (open)
- [#53772](https://github.com/vllm-project/vllm/pull/53772) "[BugFix][Core] Promote parked skipped_waiting requests under saturation" (open)
- [#53501](https://github.com/vllm-project/vllm/pull/53501) "[Bugfix][Frontend] Preserve prefix cache for inline system turns" (open)
- [#53852](https://github.com/vllm-project/vllm/pull/53852) "[Bugfix] [Perf] Honor explicit FlashInfer all-reduce size override" (open)
- [#54078](https://github.com/vllm-project/vllm/pull/54078) "[Bugfix][Frontend] Let the reasoning parser decide reasoning_ended when reasoning is hidden" (open)
- [#53799](https://github.com/vllm-project/vllm/pull/53799) "[Bugfix][Scheduler] Handle missing req_id in update_from_output gracefully" (open)
- [#53856](https://github.com/vllm-project/vllm/pull/53856) "[Bugfix][ROCm] Mask paged attention V cache padding" (open)
- [#53509](https://github.com/vllm-project/vllm/pull/53509) "[Bugfix][MoE] Restore derived buffers after weight reload" (open)
- [#53974](https://github.com/vllm-project/vllm/pull/53974) "Revert "[Bugfix][ROCm][Disagg] Fix MoRIIO shared KV memory region registration" ([#53698](https://github.com/vllm-project/vllm/pull/53698))" (open)
- [#54013](https://github.com/vllm-project/vllm/pull/54013) "[Bugfix] Drop num_stages for MLA decode with fp8 KV cache on small-smem GPUs" (open)
- [#54085](https://github.com/vllm-project/vllm/pull/54085) "[Bugfix] Clamp TurboQuant value range to fp16 before quantizing" (open)
- [#53739](https://github.com/vllm-project/vllm/pull/53739) "[Bugfix][Parser] Terminate streamed tool arguments the flush cannot extend" (open)

</details>

<details>
<summary>Tests, CI & build (41)</summary>

- [#53325](https://github.com/vllm-project/vllm/pull/53325) "Vllm recipes tool improve"
- [#53688](https://github.com/vllm-project/vllm/pull/53688) "[Agents] Add kernel microbenchmark skill"
- [#53443](https://github.com/vllm-project/vllm/pull/53443) "[CI/Build][Hardware][NVIDIA] Add opt-in Rubin Docker builds"
- [#53946](https://github.com/vllm-project/vllm/pull/53946) "[Tools][Recipes] Improve sweep recommendations and short-alias parsing"
- [#51830](https://github.com/vllm-project/vllm/pull/51830) "[CI] Report torch-nightly results to PyTorch CRCR"
- [#53712](https://github.com/vllm-project/vllm/pull/53712) "[Hardware][AMD][Perf][Bugfix] Update ROCr and clr in base image"
- [#53351](https://github.com/vllm-project/vllm/pull/53351) "[ROCm][CI] Restore attention coverage after KV-cache layout refactor"
- [#53290](https://github.com/vllm-project/vllm/pull/53290) "[CI] Preserve Rust Docker cache across commits"
- [#52547](https://github.com/vllm-project/vllm/pull/52547) "[CI][AMD] Honor single-node Docker workload timeout"
- [#53530](https://github.com/vllm-project/vllm/pull/53530) "Exclude the cpu backend from vLLM's active-Triton-driver count ([#53530](https://github.com/vllm-project/vllm/pull/53530))"
- [#53589](https://github.com/vllm-project/vllm/pull/53589) "[ROCm][CI] Skip ModernBERT FP8 MTEB test when no FP8 ScaledMM kernel exists"
- [#53732](https://github.com/vllm-project/vllm/pull/53732) "[CI] forward fix CRCR report step in the torch-nightly lane"
- [#50632](https://github.com/vllm-project/vllm/pull/50632) "[CI] Add GSM8K accuracy test for amd/DeepSeek-V4-Flash-MXFP4"
- [#49218](https://github.com/vllm-project/vllm/pull/49218) "[CI/Build][The Rock] Use model_class_overrides so spawned worker can use test PredictableLlamaForCausalLM class when worker spawned using Python 3.14"
- [#53619](https://github.com/vllm-project/vllm/pull/53619) "[Refactor] Refactor batch invariance folder"
- [#53817](https://github.com/vllm-project/vllm/pull/53817) "[XPU][Dockerfile] Update UCX install"
- [#53702](https://github.com/vllm-project/vllm/pull/53702) "[Agents] Add CUDA IMA debugging skill"
- [#49600](https://github.com/vllm-project/vllm/pull/49600) "[CI] Build mamba-ssm with C++20 for torch 2.14 nightly compatibility"
- [#53920](https://github.com/vllm-project/vllm/pull/53920) "[Benchmark] Warn on warm prefix cache for random serve runs"
- [#53358](https://github.com/vllm-project/vllm/pull/53358) "[CI/Build] Pin Cython below 3.3 for arm64 tilelang sdist"
- [#53949](https://github.com/vllm-project/vllm/pull/53949) "[Rocm][CI] add dockerfile.xpu to rocm ci artifact"
- [#53862](https://github.com/vllm-project/vllm/pull/53862) "[XPU][CI] increase timeout of extract_hidden_states tp2"
- [#53646](https://github.com/vllm-project/vllm/pull/53646) "[CI][The Rock] Increase flex attention abs tol"
- [#53618](https://github.com/vllm-project/vllm/pull/53618) "[CI] Increase Entrypoints Unit timeout after launcher suite growth"
- [#53866](https://github.com/vllm-project/vllm/pull/53866) "[CI/Build] Improve pre-commit fail message"
- [#53841](https://github.com/vllm-project/vllm/pull/53841) "[XPU][TEST]Move LoRA Multimodal to B70 in Intel GPU CI"
- [#53541](https://github.com/vllm-project/vllm/pull/53541) "[Test][RL] Add weight update E2E tests" (open)
- [#53643](https://github.com/vllm-project/vllm/pull/53643) "Add tests for MoE dispatch and Triton qzeros reshape" (open)
- [#53769](https://github.com/vllm-project/vllm/pull/53769) "[Test] Conformance suite for KV-cache key partitioning" (open)
- [#53813](https://github.com/vllm-project/vllm/pull/53813) "[Tests] Multi-GPU CI coverage lint tool (exploratory, draft)" (open)
- [#53676](https://github.com/vllm-project/vllm/pull/53676) "Bump the minor-update group across 1 directory with 175 updates" (open)
- [#53638](https://github.com/vllm-project/vllm/pull/53638) "[Test] Add a speculative-decoding x tool-calling gate" (open)
- [#53980](https://github.com/vllm-project/vllm/pull/53980) "[XPU][TEST]Add entrypoints test in Intel GPU CI" (open)
- [#53591](https://github.com/vllm-project/vllm/pull/53591) "[ROCm][CI] Keep startup profiling from aborting when free memory grows" (open)
- [#53637](https://github.com/vllm-project/vllm/pull/53637) "[Test] Add a structured-outputs x tool-calling gate" (open)
- plus 6 more minor CI updates

</details>

<details>
<summary>Docs (7)</summary>

- [#53494](https://github.com/vllm-project/vllm/pull/53494) "[XPU] update key supported models"
- [#53582](https://github.com/vllm-project/vllm/pull/53582) "[Docs][Security] Document multimodal media UUID security implications"
- [#53220](https://github.com/vllm-project/vllm/pull/53220) "[Doc] Fix local input path in run-batch examples across docs"
- [#53650](https://github.com/vllm-project/vllm/pull/53650) "[Doc] Add Granite 3.1 series to batch invariance tested models"
- [#53839](https://github.com/vllm-project/vllm/pull/53839) "[Doc] Add EXAONE-4.0-1.2B to batch invariance tested models"
- [#53226](https://github.com/vllm-project/vllm/pull/53226) "[Xeon][doc]add Xeon recipes into table"
- [#53493](https://github.com/vllm-project/vllm/pull/53493) "docs: add GPU architecture compatibility matrix and expand KServe integration guide" (open)

</details>

<details>
<summary>Refactors (6)</summary>

- [#53559](https://github.com/vllm-project/vllm/pull/53559) "[MISC] Cleanup deprecated parameters"
- [#50932](https://github.com/vllm-project/vllm/pull/50932) "buffer size insuffient Dspark sd for FlashInfer MNNVL allreduce"
- [#48687](https://github.com/vllm-project/vllm/pull/48687) "[Core] drop duplicate VLLM_USE_DEEP_GEMM check"
- [#53264](https://github.com/vllm-project/vllm/pull/53264) "[2/N][KV Connector] Identify externally transferable KV cache groups"
- [#54049](https://github.com/vllm-project/vllm/pull/54049) "draft/wip, do not review" (open)
- [#53941](https://github.com/vllm-project/vllm/pull/53941) "[Refactor] Remove utils dead code" (open)

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (vllm.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 19f7e52746cb0d9f48ac2b1715ecd3792b92c563b245d2ed0f7560faecf9f78f -->
