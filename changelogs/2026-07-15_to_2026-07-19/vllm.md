# vllm: PR digest (2026-07-15 to 2026-07-19)

_156 merged, 279 newly opened - source vllm-project/vllm, generated 2026-07-19T22:03:31Z_

## TL;DR
- **DeepSeek models** dominated attention, with major performance optimizations for sparse MLA, DSv4 routing, and KV cache offloading/compression.
- **MoE & Quantization** saw massive investments, including new NVFP4 online quantization, FP8 group quantization, and expanded support for FlashInfer and Triton backends.
- **Speculative Decoding & KV Cache** architectures advanced significantly with adaptive spec decode, multi-module MTP, DSpark/DFlare support, and disaggregated KV tiering (Mooncake/MoRIIO).
- **Hardware support** expanded across the board: AMD ROCm gained tuned AITER and MXFP4 MoE kernels, Intel XPU received batch-invariant kernels, and NVIDIA Hopper/Blackwell got specialized attention and MoE kernels.
- **Overall direction:** Hardening inference efficiency for massive MoE models through aggressive quantization (NVFP4/FP8), advanced speculative decoding, and disaggregated KV cache architectures.

## Most important PRs
- **[#48799](https://github.com/vllm-project/vllm/pull/48799)** Adds core support for the Inkling model family, including attention, MoE, multimodal, and quantization components.
- **[#46570](https://github.com/vllm-project/vllm/pull/46570)** Introduces ModelRunner V2 virtual-batch prefix caching for MLA, significantly improving prefix-caching efficiency for models like DeepSeek.
- **[#42749](https://github.com/vllm-project/vllm/pull/42749)** Fuses QK Norm, RoPE, and KV Cache for AMD ROCm, delivering a major end-to-end runtime performance win for Qwen3-30B on AITER backends.
- **[#48451](https://github.com/vllm-project/vllm/pull/48451)** Adds INT4 quantization support for the emulation MoE backend, reducing memory footprint for weight-only quantized Mixture of Experts models.
- **[#49121](https://github.com/vllm-project/vllm/pull/49121)** Implements highly sparse routed experts, introducing specialized kernels and distributed routing logic to drastically improve massive MoE efficiency on NVIDIA GPUs.

## More changes by area

<details>
<summary>Performance (18)</summary>

- [#47718](https://github.com/vllm-project/vllm/pull/47718) "[ROCm][Perf] DSv4 two-stage compressor kernel for HCA prefill"
- [#48137](https://github.com/vllm-project/vllm/pull/48137) "[Perf] Remove redundant repeat and copy for dsv4, 1.8% E2E TPOT improvement."
- [#48660](https://github.com/vllm-project/vllm/pull/48660) "[Perf] Optimize dsv4 routing using specialized kernel, 2.94% E2E TPOT improvement"
- [#47463](https://github.com/vllm-project/vllm/pull/47463) "[Perf] Optimize `fused_topk_bias` for DSv4, 1.5~2x kernel performance improvement"
- [#46832](https://github.com/vllm-project/vllm/pull/46832) "[ROCm][DSv3.2][Perf] Cap sparse MLA decode KV-splits with a work-per-split heuristic"
- [#48519](https://github.com/vllm-project/vllm/pull/48519) "[ROCm][Perf] Optimize sparse attention prefill kernel for DeepSeek-V4"
- [#48143](https://github.com/vllm-project/vllm/pull/48143) "[Perf] Optimize `clamp` to `clamp_`"
- [#48110](https://github.com/vllm-project/vllm/pull/48110) "[Perf][Hybrid] Vectorize _copy_mamba_state_block to uint64 for temporal"
- [#47156](https://github.com/vllm-project/vllm/pull/47156) "[Perf][MoE] Write FlashInfer combine into final output"
- [#48788](https://github.com/vllm-project/vllm/pull/48788) "[ROCm][Perf][DSV4] Improve sparse decode reduction occupancy on gfx950"
- [#48726](https://github.com/vllm-project/vllm/pull/48726) "[Perf][Kernel] Fused DSA indexer Top-k kernel (LiteTopk)"
- [#48928](https://github.com/vllm-project/vllm/pull/48928) "perf(spec-decode): use FlashInfer AIR for MTP top-p"
- [#48727](https://github.com/vllm-project/vllm/pull/48727) "[ROCm][Perf] Use AITER tgemm for DeepSeek V4 compressors"
- [#48887](https://github.com/vllm-project/vllm/pull/48887) "[LoRA][Perf] Zero-slice early-exit for LoRA kernels"
- [#48774](https://github.com/vllm-project/vllm/pull/48774) "[Perf] Tune LL BF16 Router GEMM"
- [#48913](https://github.com/vllm-project/vllm/pull/48913) "[Perf] Avoid full-vocab sort in the small-batch top-k/top-p sampler path"
- [#48957](https://github.com/vllm-project/vllm/pull/48957) "[DSv4 Perf] Skip empty c128 kernel launch, around 2x kernel performance improvement."
- [#49078](https://github.com/vllm-project/vllm/pull/49078) "[Perf] fused_moe: load B weights via TMA tensor descriptor on SM90+"

</details>

<details>
<summary>Kernels & attention (16)</summary>

- [#48582](https://github.com/vllm-project/vllm/pull/48582) "[M3] Improve indexer for long-context decode (sm100)"
- [#47973](https://github.com/vllm-project/vllm/pull/47973) "BF16x3 router GEMM"
- [#48385](https://github.com/vllm-project/vllm/pull/48385) "add pad-aware reduce path"
- [#48012](https://github.com/vllm-project/vllm/pull/48012) "[Attention] Allow selecting a different attention backend per KV-cache group"
- [#48858](https://github.com/vllm-project/vllm/pull/48858) "[Model] Add Hopper FA4 relative attention for Inkling"
- [#48264](https://github.com/vllm-project/vllm/pull/48264) "[Kernel][Helion] Helion kernel lazy registration"
- [#48889](https://github.com/vllm-project/vllm/pull/48889) "[HelionLinearBackend][2/N] Add helion_cutlass_hybrid_scaled_mm c++ kernel"
- [#48792](https://github.com/vllm-project/vllm/pull/48792) "[Kernel] ReplaySSM: cache SSM inputs for faster Gated DeltaNet standard decode"
- [#48994](https://github.com/vllm-project/vllm/pull/48994) "[Attention][MiniMax-M3] Add FlashInfer MSA backend for SM120/SM121"
- [#48897](https://github.com/vllm-project/vllm/pull/48897) "[Attention] Add direct symmetric-memory DCP A2A"
- [#48770](https://github.com/vllm-project/vllm/pull/48770) "[2/N][Attention] Enable masked MHA for sparse MLA prefills"
- [#48980](https://github.com/vllm-project/vllm/pull/48980) "[WIP] Add mamba ssu kernel autotune at warmup time"
- [#48995](https://github.com/vllm-project/vllm/pull/48995) "[Helion] Route fusion-only kernels to Helion during CUDA-graph capture"
- [#48979](https://github.com/vllm-project/vllm/pull/48979) "skip cudagraph/DP padding in topk"
- [#49087](https://github.com/vllm-project/vllm/pull/49087) "[Kernel][MoE] Zero-expert identity: drop redundant zeros_like, use ceil-div grid"
- [#48997](https://github.com/vllm-project/vllm/pull/48997) "[Bugfix] Pin RMSNorm block size under batch invariance"

</details>

<details>
<summary>MoE & quantization (18)</summary>

- [#48538](https://github.com/vllm-project/vllm/pull/48538) "[Quant] Add `nvfp4_per_token` online MoE quantization"
- [#46390](https://github.com/vllm-project/vllm/pull/46390) "[Quant] Enable humming w[2-7]a[4,8] inference with compressed-tensors"
- [#48632](https://github.com/vllm-project/vllm/pull/48632) "[LoRA][1/N] Integrate flashinfer MoE LoRA for BF16 model"
- [#48990](https://github.com/vllm-project/vllm/pull/48990) "[Model] Use standard ModelOpt config for Inkling NVFP4"
- [#47881](https://github.com/vllm-project/vllm/pull/47881) "[Feature] Migrate moe sp support to non-torch compiled path for GLM5.2"
- [#48797](https://github.com/vllm-project/vllm/pull/48797) "[Kernel][Helion] Disable warp specialization in rms_norm_per_block_quant B200 configs"
- [#48991](https://github.com/vllm-project/vllm/pull/48991) "[Kernel][Helion] Add packed per-token group FP8 quant"
- [#49086](https://github.com/vllm-project/vllm/pull/49086) "[ROCm][feature] Add new moe backends supporting int4/int8 weight-only…"
- [#49060](https://github.com/vllm-project/vllm/pull/49060) "[Quant] Add online NVFP4 dense-linear quantization (W4A16 + W4A4)"
- [#48964](https://github.com/vllm-project/vllm/pull/48964) "[Kernel][Helion] Retune dynamic quant schedules on H100"
- [#48900](https://github.com/vllm-project/vllm/pull/48900) "[Kernel][Helion] Retune grouped quant schedules"
- [#48963](https://github.com/vllm-project/vllm/pull/48963) "[DO NOT REVIEW][Kernel][Helion] Retune SiLU FP8 schedules on H100"
- [#48728](https://github.com/vllm-project/vllm/pull/48728) "[ROCm][Perf][DeepSeek V4] Fuse native FP8 shared expert into AITER MXFP4 MoE"
- [#48870](https://github.com/vllm-project/vllm/pull/48870) "[Model][Quant] Fused WNA16 GEMM for tied quantized lm_head logits"
- [#49099](https://github.com/vllm-project/vllm/pull/49099) "Improve SM90 NVFP4 Marlin MoE wide-N alignment"
- [#48918](https://github.com/vllm-project/vllm/pull/48918) "[CT] Support Humming for WNA16 MoE"
- [#48983](https://github.com/vllm-project/vllm/pull/48983) "[Kernel] Opt-in FP8 requant of bf16 attention proj on NVFP4 checkpoints"
- [#48876](https://github.com/vllm-project/vllm/pull/48876) "Inkling FP8 Compressed Tensors Support"

</details>

<details>
<summary>Model support (12)</summary>

- [#48869](https://github.com/vllm-project/vllm/pull/48869) "[Model] Add Inkling MTP=1 support [3/N]"
- [#48884](https://github.com/vllm-project/vllm/pull/48884) "[Model] Add Inkling LoRA support [4/N]"
- [#48822](https://github.com/vllm-project/vllm/pull/48822) "[Model] Add PW CUDA graph support for Inkling [2/N]"
- [#47991](https://github.com/vllm-project/vllm/pull/47991) "[Model] Add RobertaForTokenClassification / XLMRobertaForTokenClassification"
- [#41599](https://github.com/vllm-project/vllm/pull/41599) "[Model] Support TranslateGemma-12b-it"
- [#48841](https://github.com/vllm-project/vllm/pull/48841) "[ROCm] [Model] Enable TML inkling"
- [#48686](https://github.com/vllm-project/vllm/pull/48686) "[Model] Add minimal native RWKV7 serving support"
- [#48999](https://github.com/vllm-project/vllm/pull/48999) "[Model] Add MiniCPM-SALA (hybrid Lightning Attention + InfLLM-V2-ready GQA)"
- [#48768](https://github.com/vllm-project/vllm/pull/48768) "[Model] Add Inkling multi-depth MTP support [5/N]"
- [#48954](https://github.com/vllm-project/vllm/pull/48954) "[ROCm][Model] Add Inkling BF16 support"
- [#48939](https://github.com/vllm-project/vllm/pull/48939) "[ROCm] Support MiniMax-M3 NVFP4 SwiGLU-OAI"
- [#48952](https://github.com/vllm-project/vllm/pull/48952) "Cosmos3 FP8 ModelOpt/Diffusers remapping"

</details>

<details>
<summary>Parallelism & scheduling (16)</summary>

- [#48150](https://github.com/vllm-project/vllm/pull/48150) "[KV Offload] Define clean backend configuration boundary"
- [#48281](https://github.com/vllm-project/vllm/pull/48281) "[KV Offload] Add optional tier locality to FS/OBJ KV events"
- [#47636](https://github.com/vllm-project/vllm/pull/47636) "[KVOffload][P2P] Well-known default host/port env vars and per-DP-rank control port"
- [#48878](https://github.com/vllm-project/vllm/pull/48878) "Add blocks_per_chunk configuration for KV offloading to support heterogeneous KV cache groups"
- [#48209](https://github.com/vllm-project/vllm/pull/48209) "Vectorize prep xfer list creation"
- [#48715](https://github.com/vllm-project/vllm/pull/48715) "Dynamic-fork scheduling, Medusa/MTP spec decode, and InternVL resize for HPD-Parsing (based on v0.17.1)"
- [#48906](https://github.com/vllm-project/vllm/pull/48906) "[KV Offload] Deduplicate replicated MLA KV in the shared CPU region"
- [#48679](https://github.com/vllm-project/vllm/pull/48679) "[KV Offload] Support self-describing KV events with TieringOffloadingSpec"
- [#49109](https://github.com/vllm-project/vllm/pull/49109) "[KV Connector][Mooncake] Add PCP-aware worker discovery"
- [#49123](https://github.com/vllm-project/vllm/pull/49123) "Add SparDA lookahead KV connector"
- [#48877](https://github.com/vllm-project/vllm/pull/48877) "[Core] Add opt-in eager PyNccl TP all-reduce split for PIECEWISE CUDA graphs"
- [#48704](https://github.com/vllm-project/vllm/pull/48704) "[Feature] Support prompt cache retention policies for tiered KV offloading"
- [#48933](https://github.com/vllm-project/vllm/pull/48933) "[Core] Add remaining copy counts to KV removal events"
- [#49114](https://github.com/vllm-project/vllm/pull/49114) "Add CachePolicyFactory for pluggable/external eviction policies"
- [#49075](https://github.com/vllm-project/vllm/pull/49075) "[V1][Scheduler] Enforce max_num_partial_prefills and max_long_partial_prefills"
- [#49009](https://github.com/vllm-project/vllm/pull/49009) "Support sequence parallelism for block fp8 on XPU"

</details>

<details>
<summary>Hardware & arch (7)</summary>

- [#48159](https://github.com/vllm-project/vllm/pull/48159) "[ROCm] Add tuned selective_state_update config for AMD MI350"
- [#48526](https://github.com/vllm-project/vllm/pull/48526) "[ROCm] Re-enable cudagraph memory profiling, captured on the current stream"
- [#47975](https://github.com/vllm-project/vllm/pull/47975) "[XPU] support HND layout"
- [#48828](https://github.com/vllm-project/vllm/pull/48828) "[XPU] allow forcing flash attn for mm_prefix"
- [#49077](https://github.com/vllm-project/vllm/pull/49077) "TRITON_ATTN support for KV cache dtype fp8 on SM75 to pre-SM89"
- [#48757](https://github.com/vllm-project/vllm/pull/48757) "[ROCm][Compilation]Fuse Transformers Residual Add, RMSNorm, and FP8 Quantization"
- [#48989](https://github.com/vllm-project/vllm/pull/48989) "[Draft][ROCm] DeepSeek-V4-Pro PD Disaggregation through MORI IO KV Connector on AMD GPUs"

</details>

<details>
<summary>API & serving (24)</summary>

- [#48107](https://github.com/vllm-project/vllm/pull/48107) "[Rust][Benchmark] Port in vllm-bench"
- [#48554](https://github.com/vllm-project/vllm/pull/48554) "[Rust Frontend] Integrate MM audio support"
- [#47699](https://github.com/vllm-project/vllm/pull/47699) "[Frontend] Overlap preprocessing and computation for pooling models offline inference"
- [#48042](https://github.com/vllm-project/vllm/pull/48042) "[rl] Stateful Trainer Send: New Abstractions [1/N]"
- [#48617](https://github.com/vllm-project/vllm/pull/48617) "[Render] Add round trip parity test and docs for derender"
- [#47741](https://github.com/vllm-project/vllm/pull/47741) "[Rust Frontend] Add Seed-OSS tool parser"
- [#48535](https://github.com/vllm-project/vllm/pull/48535) "[Front-end] [Messages] Populate `num_cache_creation_tokens`"
- [#48034](https://github.com/vllm-project/vllm/pull/48034) "[Rust Frontend] Tolerate whitespace before the outer brace in JSON tool-call parsers"
- [#48174](https://github.com/vllm-project/vllm/pull/48174) "Build with ABI stable FlashMLA"
- [#48947](https://github.com/vllm-project/vllm/pull/48947) "[PARSER][Mistral] unified engine-based parser for reasoning and tool calls"
- [#48996](https://github.com/vllm-project/vllm/pull/48996) "[Frontend] Add vllm snapshot create and opt-in CRIU restore for serve"
- [#48789](https://github.com/vllm-project/vllm/pull/48789) "[Profiler] Add Triton Proton profiling backend"
- [#48867](https://github.com/vllm-project/vllm/pull/48867) "[Metrics] Add --custom-histogram-buckets to override histogram bucket families"
- [#48866](https://github.com/vllm-project/vllm/pull/48866) "[Metrics] Consolidate Prometheus histogram bucket defaults into a single module"
- [#48981](https://github.com/vllm-project/vllm/pull/48981) "[rl] Stateful Trainer Send: IPC [2/N]"
- [#49037](https://github.com/vllm-project/vllm/pull/49037) "[Perf] Add per-phase cold-start startup span benchmark harness"
- [#48937](https://github.com/vllm-project/vllm/pull/48937) "[Rust][Benchmark] Use `tracing` for logs"
- [#48930](https://github.com/vllm-project/vllm/pull/48930) "[Rust][Benchmark] Integrate `vllm-bench` to `vllm-rs` & `vllm` CLI"
- [#48915](https://github.com/vllm-project/vllm/pull/48915) "[Frontend][Core][Spec Decode] Per-request acceptance stats in OpenAI API responses"
- [#48992](https://github.com/vllm-project/vllm/pull/48992) "[Rust Frontend] Add engine-aware health reporting"
- [#49040](https://github.com/vllm-project/vllm/pull/49040) "[Core][Frontend] Add weight version tagging for RL rollouts"
- [#48969](https://github.com/vllm-project/vllm/pull/48969) "Add pushed-based ZMQ metrics logger support"
- [#49124](https://github.com/vllm-project/vllm/pull/49124) "[UX] Improve data-parallel launch validation"
- [#48800](https://github.com/vllm-project/vllm/pull/48800) "[Rust Frontend] Add hy_v3 reasoning parser"

</details>

<details>
<summary>Speculative Decoding (8)</summary>

- [#47677](https://github.com/vllm-project/vllm/pull/47677) "[XPU] Add DSpark speculative decoding support for DeepSeek-V4"
- [#47216](https://github.com/vllm-project/vllm/pull/47216) "[Spec Decode][DSpark] Add Gemma4-12B DSpark draft model"
- [#48787](https://github.com/vllm-project/vllm/pull/48787) "[Spec Decode] Add kv_cache_dtype to speculative_config to control separately from target"
- [#48892](https://github.com/vllm-project/vllm/pull/48892) "[WIP][Model Runner V2][Spec Decode] Add multi-module MTP support"
- [#48692](https://github.com/vllm-project/vllm/pull/48692) "[MRV2][Spec Decode] Adaptive Speculative Decoding - Initial Support"
- [#49023](https://github.com/vllm-project/vllm/pull/49023) "[Feat][Spec Decode] Add DFlare support for Qwen3 series"
- [#48944](https://github.com/vllm-project/vllm/pull/48944) "[Spec Decode] Context-length-aware K in DSD (RFC #48627): extend num_speculative_tokens_per_batch_size with a ctx axis"
- [#48804](https://github.com/vllm-project/vllm/pull/48804) "[Spec Decode][V1] Warm Eagle spec-decode Triton kernels at startup"

</details>

<details>
<summary>Refactors (9)</summary>

- [#48496](https://github.com/vllm-project/vllm/pull/48496) "Remove even more unnecessary `load_weights` methods"
- [#46647](https://github.com/vllm-project/vllm/pull/46647) "[Refactor] Move iteration logging to the frontend"
- [#48780](https://github.com/vllm-project/vllm/pull/48780) "[Refactor] Remove deepseek dead code"
- [#49003](https://github.com/vllm-project/vllm/pull/49003) "[Refactor] Extract StructuredOutputsParams creation logic from Request.to_sampling_params"
- [#48500](https://github.com/vllm-project/vllm/pull/48500) "[Refactor] Move fla to third party"
- [#49038](https://github.com/vllm-project/vllm/pull/49038) "Make `load_weights` completely optional"
- [#48949](https://github.com/vllm-project/vllm/pull/48949) "[ROCm][Quantization][5/N] Refactor `QuarkOCP_MX` to use MXFP4 linear kernel abstraction"
- [#49045](https://github.com/vllm-project/vllm/pull/49045) "[Rust Frontend] Extract request preparation from the inference path"
- [#48781](https://github.com/vllm-project/vllm/pull/48781) "[Rust Frontend] Use zero-copy slicing for multimodal tensors"

</details>

<details>
<summary>Bugfixes (90)</summary>

- [#49026](https://github.com/vllm-project/vllm/pull/49026) "[Bugfix][Platform] sm12x: add FLASHMLA_SPARSE (Triton sparse-MLA) to the MLA-sparse backend candidate list — flashinfer sparse_mla_sm120 livelocks on GB10"
- [#48642](https://github.com/vllm-project/vllm/pull/48642) "[Bugfix] Sparse MLA: enable fp8_ds_mla dense prefill"
- [#46213](https://github.com/vllm-project/vllm/pull/46213) "[Bugfix][Multimodal] Fix Qwen3-Omni use_audio_in_video with mixed image/video inputs"
- [#46115](https://github.com/vllm-project/vllm/pull/46115) "[Bugfix] MoRIIO toy P/D proxy: fix DP-rank index aliasing + harden for high-concurrency bursts"
- [#48167](https://github.com/vllm-project/vllm/pull/48167) "[Bugfix] Fix FlashInfer non-causal draft attention (DFlash/DSpark) on Blackwell"
- [#47770](https://github.com/vllm-project/vllm/pull/47770) "[ROCm][BugFix] Triton W4A16 handling for GPTQ/AutoGPTQ qzeros layout"
- [#48846](https://github.com/vllm-project/vllm/pull/48846) "[Bugfix][Tool Parser] Preserve whitespace in parameter values (MiniMax M2, Qwen3, MiniCPM5 XML)"
- [#48481](https://github.com/vllm-project/vllm/pull/48481) "[KV Connector] Fix PD async scheduling race condition for hybrid attn models"
- [#44371](https://github.com/vllm-project/vllm/pull/44371) "[Bugfix] Preserve unloaded non-persistent buffers during layerwise reload"
- [#48596](https://github.com/vllm-project/vllm/pull/48596) "[Bugfix][KV Offloading] Offload last block at request finish and prevent reuse race"
- [#47680](https://github.com/vllm-project/vllm/pull/47680) "[Bugfix][V1/V2] Fix prompt_logprobs to respect logprobs_mode"
- [#48984](https://github.com/vllm-project/vllm/pull/48984) "[Bugfix] Reject removed pooling parameters"
- [#48729](https://github.com/vllm-project/vllm/pull/48729) "[Bugfix][GLM4V] Fix video dummy profiling and memory usage"
- [#48671](https://github.com/vllm-project/vllm/pull/48671) "[Bugfix][Spec Decode] Support heterogeneous QK fusion geometry"
- [#47495](https://github.com/vllm-project/vllm/pull/47495) "[Bugfix][KV-transfer] MoRIIO: retry RDMA send-queue-full backpressure instead of failing the read"
- plus 75 more minor bugfixes

</details>

<details>
<summary>Tests, CI & build (35)</summary>

- [#49044](https://github.com/vllm-project/vllm/pull/49044) "[ROCm] [Release] [Per-commit] Reenable per commit rocm wheel"
- [#48387](https://github.com/vllm-project/vllm/pull/48387) "[CI][AMD] Configure MI300 tests for native execution without DinD"
- [#44549](https://github.com/vllm-project/vllm/pull/44549) "[Security] Replace diskcache to eliminate pickle deserialization"
- [#47442](https://github.com/vllm-project/vllm/pull/47442) "[CI/Build][Docker] Bump nvidia-cutlass-dsl to 4.6.0 and drop packaging workarounds"
- [#48772](https://github.com/vllm-project/vllm/pull/48772) "[CI] Gate non-default release wheel builds"
- [#48746](https://github.com/vllm-project/vllm/pull/48746) "[CI][ROCm] Stabilize ci_base hash calculation and image handoff"
- [#47669](https://github.com/vllm-project/vllm/pull/47669) "Bump flashinfer version to 0.6.14"
- [#47330](https://github.com/vllm-project/vllm/pull/47330) "[ROCm][CI] Remove mxfp4 test skips after `amd-quark` 0.12 release"
- [#48600](https://github.com/vllm-project/vllm/pull/48600) "[CI/Build] Split release artifact annotations by type"
- [#46868](https://github.com/vllm-project/vllm/pull/46868) "[Loader] Improve InstantTensor loading"
- plus 25 more minor CI and test updates

</details>

<details>
<summary>Docs & Other (45)</summary>

- [#48497](https://github.com/vllm-project/vllm/pull/48497) "[Docs] Document pooling config resolution"
- [#44749](https://github.com/vllm-project/vllm/pull/44749) "[Misc] Remove orphaned env vars and stale env-var references"
- [#48839](https://github.com/vllm-project/vllm/pull/48839) "[docs] preserve page path in stable-docs announcement link"
- [#49024](https://github.com/vllm-project/vllm/pull/49024) "[Doc] Add stream tracker middleware example for live per-request visibility"
- [#48790](https://github.com/vllm-project/vllm/pull/48790) "[Doc]: Add Pixeltable integration to inference & serving/integrations docs"
- [#49066](https://github.com/vllm-project/vllm/pull/49066) "[docs] Add documentation for pynvvideocodec video decoding backend"
- [#48782](https://github.com/vllm-project/vllm/pull/48782) "[Doc] Expand ModelOpt NVFP4 docs: hardware support, MoE serving, accuracy evaluation"
- [#48925](https://github.com/vllm-project/vllm/pull/48925) "Skill to check for prebuilt wheels during installation"
- [#48512](https://github.com/vllm-project/vllm/pull/48512) "[Kernel][Helion] Add Helion kernel benchmark script"
- [#48759](https://github.com/vllm-project/vllm/pull/48759) "[LoRA] Optimize TrtLlmLoRAExperts"
- plus 35 more minor docs and misc updates

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (vllm.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 0478a20c2750325e519fca4e9e1a8c131ec301a4649fd7748dd1ecc2777a7e09 -->
