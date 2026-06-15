# sglang: PR digest (2026-06-10 to 2026-06-14)

_246 merged, 235 newly opened - source sgl-project/sglang, generated 2026-06-14T22:30:31Z_

## TL;DR
- **Model focus**: DeepSeek (V3/V4) dominated attention with 46 PRs, gaining BF16 KV cache decode paths, W4A8 MXFP4 MoE backends, and Ascend NPU support. MiniMax-M3, Gemma 4, and GLM-5.1 also saw significant feature work.
- **Speculative Decoding**: A major architectural shift is underway, retiring Spec V1 and EAGLE v1 in favor of Spec V2, DFlash, and Ngram spec v2, alongside new CPU-based speculative decoding support.
- **Quantization & MoE**: Heavy investments in ultra-low precision, including online MXFP4 requantization on AMD, NVFP4 on NVIDIA, and tuned fused-MoE Triton kernels for SM120/SM121.
- **Hardware & Architecture**: Broad hardware optimizations landed, including Ascend NPU DeepSeek-V4-Flash support, Intel XPU Triton chunked implementations, and AMD unified KV attention.
- **Overall direction**: The engine is aggressively optimizing for next-gen hardware (SM120, AMD gfx950) and ultra-low precision (FP4/FP8) while completely revamping its speculative decoding and caching (HiCache/UnifiedTree) infrastructure.

## Most important PRs
- **[#27944](https://github.com/sgl-project/sglang/pull/27944)** (opened) adds comprehensive support for the MiniMax-M3 model, including Triton attention, distributed frontend, and MoE kernels across AMD and NVIDIA hardware.
- **[#23906](https://github.com/sgl-project/sglang/pull/23906)** refactors the CUDA Graph Runner and Backend, touching over 160 files to unify attention, distributed, and speculative decoding paths across FlashInfer and Triton backends.
- **[#27904](https://github.com/sgl-project/sglang/pull/27904)** (opened) introduces Ascend NPU support for the DeepSeek-V4-Flash architecture, enabling attention, MoE, and speculative decoding on Huawei hardware.
- **[#26083](https://github.com/sgl-project/sglang/pull/26083)** implements online NVFP4 quantization, integrating with FlashInfer and MoE kernels to support ultra-low precision inference on NVIDIA GPUs.
- **[#23000](https://github.com/sgl-project/sglang/pull/23000)** ships Spec V2 DFlash support, integrating Triton-backed speculative decoding with the scheduler and frontend for AMD and NVIDIA targets.

## More changes by area

<details>
<summary>Performance (19)</summary>

- [#28123](https://github.com/sgl-project/sglang/pull/28123) tightens performance baselines for diffusion tests
- [#26706](https://github.com/sgl-project/sglang/pull/26706) adds a multi-GPU test and benchmark framework for custom all-reduce and TP QKNorm
- [#27965](https://github.com/sgl-project/sglang/pull/27965) reduces overhead of fill_ids list reconstruction and decref
- [#27656](https://github.com/sgl-project/sglang/pull/27656) fuses QK RMSNorm and gate extraction into a single Triton kernel for Qwen3.5 on HIP
- [#27896](https://github.com/sgl-project/sglang/pull/27896) skips per-call mat_a/scales_a padding in cutlass FP8 blockwise GEMM
- [#28169](https://github.com/sgl-project/sglang/pull/28169) reduces attention backend log noise to improve UX
- [#26082](https://github.com/sgl-project/sglang/pull/26082) eliminates CUDA syncs in the VLM embed path
- [#28076](https://github.com/sgl-project/sglang/pull/28076) removes several host-to-device syncs
- [#28079](https://github.com/sgl-project/sglang/pull/28079) (opened) invokes aiter's wi4a16 MoE kernel for significant performance improvements on Kimi-K2 class models
- [#27818](https://github.com/sgl-project/sglang/pull/27818) (opened) fuses FP8 quantization with UE8M0 scale layout for DeepSeek-V4
- [#27776](https://github.com/sgl-project/sglang/pull/27776) (opened) removes sampler hot-path sync for custom logit processors
- [#28057](https://github.com/sgl-project/sglang/pull/28057) (opened) uses unflattened DeepGEMM next-n layout on SM100 for DeepSeek-V4
- [#27926](https://github.com/sgl-project/sglang/pull/27926) (opened) makes FP8 quant output tensor contiguous for DeepSeek-V4
- [#28136](https://github.com/sgl-project/sglang/pull/28136) (opened) reduces RoPE cache size for shorter context lengths
- [#28030](https://github.com/sgl-project/sglang/pull/28030) (opened) adds `--disable-cuda-perf-boost` to recover idle GPU power
- [#28056](https://github.com/sgl-project/sglang/pull/28056) (opened) reuses a pooled HTTP session for multimodal URL downloads
- [#28050](https://github.com/sgl-project/sglang/pull/28050) (opened) uses default torch compile mode for LTX diffusion
- [#27793](https://github.com/sgl-project/sglang/pull/27793) (opened) tunes extend attention block sizes for gfx950 (head_dim > 128)
- [#27948](https://github.com/sgl-project/sglang/pull/27948) (opened) skips custom all-reduce v2 CUDA graph capture with torch memory saver
</details>

<details>
<summary>Kernels & attention (33)</summary>

- [#27488](https://github.com/sgl-project/sglang/pull/27488) adds CuteDSL prefill kernel on SM100
- [#27380](https://github.com/sgl-project/sglang/pull/27380) adds unified KV attention support in dpsk-v4 for AMD
- [#27429](https://github.com/sgl-project/sglang/pull/27429) centralizes more inline Triton kernels for Codex
- [#27617](https://github.com/sgl-project/sglang/pull/27617) caches full-to-SWA out_cache_loc per forward across attention backends
- [#26147](https://github.com/sgl-project/sglang/pull/26147) adds Gemma4 Sliding Window Attention support on Ascend backend
- [#24955](https://github.com/sgl-project/sglang/pull/24955) supports Nemotron DP attention and MTP
- [#27695](https://github.com/sgl-project/sglang/pull/27695) bundles set_kv_buffer write targets into KVWriteLoc
- [#26924](https://github.com/sgl-project/sglang/pull/26924) overlaps mamba verify update with draft extend for Qwen3.5Opt
- [#27745](https://github.com/sgl-project/sglang/pull/27745) adds multi-arch ROCm kernel support with runtime optimization
- [#27510](https://github.com/sgl-project/sglang/pull/27510) enables DP attention, TBO, and shared experts fusion for DeepSeek
- [#27739](https://github.com/sgl-project/sglang/pull/27739) revises step3.5 flash for graph mode and uses triton activation
- [#27630](https://github.com/sgl-project/sglang/pull/27630) fuses sigmoid and mul attention output gate into a single Triton kernel for AMD
- [#27646](https://github.com/sgl-project/sglang/pull/27646) adds sycl mrope pass for Intel XPU devices
- [#28033](https://github.com/sgl-project/sglang/pull/28033) (opened) supports BF16 KV cache decode path for DeepSeek-V4
- [#27992](https://github.com/sgl-project/sglang/pull/27992) (opened) adds FlashInfer trtllm-gen skip-softmax attention backend for DiT
- [#27942](https://github.com/sgl-project/sglang/pull/27942) (opened) supports topk > 1 (EAGLE tree) in the trtllm_mha attention backend
- [#28187](https://github.com/sgl-project/sglang/pull/28187) (opened) adds int8 W8A8 SM90 swap-AB dispatch for small-M decode
- [#28025](https://github.com/sgl-project/sglang/pull/28025) (opened) adds FlashInfer MXFP4 path with custom SM120 FlashMLA for DeepSeek-V4-Flash
- [#27914](https://github.com/sgl-project/sglang/pull/27914) (opened) adds triton chunked implementation for flash_mla_with_kvcache_triton on Intel XPU
- [#28124](https://github.com/sgl-project/sglang/pull/28124) (opened) adds GQA-grouped split-K verify kernel for EAGLE3/MTP extend attention on AMD
- [#27975](https://github.com/sgl-project/sglang/pull/27975) (opened) adds `--mamba-ssm-enable-stochastic-rounding` for GDN and Mamba1/2 decode
- [#28059](https://github.com/sgl-project/sglang/pull/28059) (opened) supports fp8_paged_mqa_logits_triton on Intel XPU
- [#28106](https://github.com/sgl-project/sglang/pull/28106) (opened) makes seq_lens_cpu optional in trtllm_mha backend
- [#28049](https://github.com/sgl-project/sglang/pull/28049) (opened) adds LiteAttention-ROCM backend
- [#27963](https://github.com/sgl-project/sglang/pull/27963) (opened) covers diffkv and attention-sink triton attention kernels in tests
- [#28040](https://github.com/sgl-project/sglang/pull/28040) (opened) adds torch implementation for fused_k_norm_rope_flashmla on Intel XPU
- [#28176](https://github.com/sgl-project/sglang/pull/28176) (opened) supports native attention for Mistral3 encoder
- [#27928](https://github.com/sgl-project/sglang/pull/27928) (opened) adds prefill context parallel support for DeepSeek-V4 unified KV attention on AMD
- [#27790](https://github.com/sgl-project/sglang/pull/27790) (opened) adds torch implementation for fused_q_norm_rope on Intel XPU
- [#28137](https://github.com/sgl-project/sglang/pull/28137) (opened) adds SM120/SM121 dispatch for int8_scaled_mm
- [#28046](https://github.com/sgl-project/sglang/pull/28046) (opened) adds dsa_indexer torch Hadamard implementation for Intel XPU
- [#27870](https://github.com/sgl-project/sglang/pull/27870) (opened) adds XPU cache/sync path for set_embed_and_head for Qwen3.5
- [#27783](https://github.com/sgl-project/sglang/pull/27783) (opened) supports hc_split_sinkhorn on Intel XPU using sgl_kernel
</details>

<details>
<summary>MoE & quantization (24)</summary>

- [#18182](https://github.com/sgl-project/sglang/pull/18182) implements online MXFP4 quantization (FP8 to MXFP4 requantization) on AMD GPUs
- [#28213](https://github.com/sgl-project/sglang/pull/28213) reverts the online MXFP4 quantization on AMD GPUs
- [#26188](https://github.com/sgl-project/sglang/pull/26188) fuses SwiGLU activation into gate gather_qmv for SwitchGLU MoE blocks on Apple Silicon
- [#27449](https://github.com/sgl-project/sglang/pull/27449) supports per token group quant 8bit v2 jit kernel
- [#27720](https://github.com/sgl-project/sglang/pull/27720) defers MoE finalize and fuses it with main stream add for DeepSeek V3
- [#26204](https://github.com/sgl-project/sglang/pull/26204) optimizes Qwen3 Next FP8 MoE on H200
- [#22985](https://github.com/sgl-project/sglang/pull/22985) supports eplb for moriep on AMD
- [#27590](https://github.com/sgl-project/sglang/pull/27590) uses fused FP8 GEMM for Ideogram4 weight-only linears
- [#27057](https://github.com/sgl-project/sglang/pull/27057) moves shared expert check function to quark for AMD
- [#27107](https://github.com/sgl-project/sglang/pull/27107) enables fabric handles automatically when supported for DeepEP
- [#28101](https://github.com/sgl-project/sglang/pull/28101) (opened) enables fused Add+RMSNorm+per-token FP8 quant for checkpoint-quantized models
- [#27946](https://github.com/sgl-project/sglang/pull/27946) (opened) adds native MXFP4 expert runtime for the MiMo-V2.5 Pro FP4 target
- [#27806](https://github.com/sgl-project/sglang/pull/27806) (opened) adds W4A8 MXFP4 MoE backend for DeepSeek-V4 on SM90 via FlashInfer
- [#28155](https://github.com/sgl-project/sglang/pull/28155) (opened) adds expert-grouped GEMM for MXFP4 MoE prefill on SM120
- [#28084](https://github.com/sgl-project/sglang/pull/28084) (opened) fuses topk padded-token masking into a single Triton kernel for AMD
- [#27873](https://github.com/sgl-project/sglang/pull/27873) (opened) adds torch implementation for fused_q_indexer_rope_hadamard_quant on Intel XPU
- [#28125](https://github.com/sgl-project/sglang/pull/28125) (opened) adds SM120/SM121 dispatch for fp8_blockwise_scaled_grouped_mm
- [#28038](https://github.com/sgl-project/sglang/pull/28038) (opened) clamps default fused-MoE Triton configs to the device shared memory limit
- [#27906](https://github.com/sgl-project/sglang/pull/27906) (opened) supports Qwen3.6 ModelOpt mixed NVFP4
- [#28189](https://github.com/sgl-project/sglang/pull/28189) (opened) adds tuned fp8_w8a8 block-wise GEMM configs for RTX PRO 6000 Blackwell Max-Q
- [#28077](https://github.com/sgl-project/sglang/pull/28077) (opened) adds tuned fused-MoE Triton config for Gemma-4 FP8 on RTX PRO 6000 Blackwell
- [#27939](https://github.com/sgl-project/sglang/pull/27939) (opened) supports online MXFP8 quantization for ungated MoE
- [#27932](https://github.com/sgl-project/sglang/pull/27932) (opened) implements Mxfp4MoEMethod.get_triton_quant_info for MoE LoRA
- [#28188](https://github.com/sgl-project/sglang/pull/28188) (opened) skips eplb bookkeeping and topk remap when EPLB is not in use on mori-ep for AMD
</details>

<details>
<summary>Model support (23)</summary>

- [#26347](https://github.com/sgl-project/sglang/pull/26347) supports Zyphra zaya1 model
- [#26278](https://github.com/sgl-project/sglang/pull/26278) supports MiMo v2 ASR
- [#27409](https://github.com/sgl-project/sglang/pull/27409) adds lfm2.5 to new cookbook
- [#28064](https://github.com/sgl-project/sglang/pull/28064) adds Kimi K2.7 Code cookbook
- [#27892](https://github.com/sgl-project/sglang/pull/27892) reverts tensor parallel support for Mistral3 diffusion text encoder
- [#25950](https://github.com/sgl-project/sglang/pull/25950) adds tensor parallel support for Mistral3 diffusion text encoder
- [#27378](https://github.com/sgl-project/sglang/pull/27378) supports HiCache for MiMo-V2 models
- [#25455](https://github.com/sgl-project/sglang/pull/25455) adapts MiMo-V2-Flash for NPU
- [#27826](https://github.com/sgl-project/sglang/pull/27826) optimizes FLUX.1 tensor parallel sharding
- [#27714](https://github.com/sgl-project/sglang/pull/27714) adds Kimi-K2.6 NVFP4 and updates Kimi-K2.5 cookbook guidance
- [#27708](https://github.com/sgl-project/sglang/pull/27708) adds GLM-5.1 NVFP4 to cookbook
- [#28149](https://github.com/sgl-project/sglang/pull/28149) supports GLM-4.7 function calling via structural tags
- [#28110](https://github.com/sgl-project/sglang/pull/28110) supports DSA indexer LoRA targets for GLM-5.1 and DeepSeek-V3.2-family models
- [#28054](https://github.com/sgl-project/sglang/pull/28054) (opened) supports DiffusionGemma (google/diffusiongemma-26B-A4B-it)
- [#27887](https://github.com/sgl-project/sglang/pull/27887) (opened) adds HrmTextForCausalLM (Hierarchical Reasoning Model - Text)
- [#28199](https://github.com/sgl-project/sglang/pull/28199) (opened) supports Gemma 4 native LoRA adapters without v_proj weights
- [#28100](https://github.com/sgl-project/sglang/pull/28100) (opened) supports plain fused qkv_proj checkpoints for MiMo-V2
- [#27813](https://github.com/sgl-project/sglang/pull/27813) (opened) adds LoRA support for LFM2 and LFM2-MoE
- [#28166](https://github.com/sgl-project/sglang/pull/28166) (opened) fuses FeedForward GELU into up-proj GEMM for FLUX
- [#28164](https://github.com/sgl-project/sglang/pull/28164) (opened) fuses FeedForward GELU into up-proj GEMM for Qwen-Image
- [#28167](https://github.com/sgl-project/sglang/pull/28167) (opened) fuses gelu-approximate into up-proj GEMM for GLM-Image
- [#27976](https://github.com/sgl-project/sglang/pull/27976) (opened) adds DeepSeek V4, Qwen 3.5, and Kimi K2.5/2.6 support to ReasoningParser
- [#28007](https://github.com/sgl-project/sglang/pull/28007) (opened) enables fused QK RMSNorm path for Qwen3.5 on Intel XPU
</details>

<details>
<summary>Parallelism & scheduling (40)</summary>

- [#28133](https://github.com/sgl-project/sglang/pull/28133) clears dead DRAFT_EXTEND objects left after EAGLE v1 removal
- [#28129](https://github.com/sgl-project/sglang/pull/28129) removes deprecated EAGLE v1 DRAFT_EXTEND forward mode
- [#27950](https://github.com/sgl-project/sglang/pull/27950) folds the DFLASH worker base into DFlashWorkerV2 on BaseSpecWorker
- [#27959](https://github.com/sgl-project/sglang/pull/27959) removes the DFLASH V1 worker path
- [#27977](https://github.com/sgl-project/sglang/pull/27977) removes the dead spec V1 scheduler paths
- [#17260](https://github.com/sgl-project/sglang/pull/17260) supports ngram spec v2
- [#27469](https://github.com/sgl-project/sglang/pull/27469) adds sliding window attention draft layer support for dflash
- [#27964](https://github.com/sgl-project/sglang/pull/27964) retires Spec V1
- [#27749](https://github.com/sgl-project/sglang/pull/27749) updates weights from distributed for speculative draft workers
- [#28105](https://github.com/sgl-project/sglang/pull/28105) moves `prepare_for_draft` to `EagleDraftWorkerBase`
- [#27966](https://github.com/sgl-project/sglang/pull/27966) dedups post-verify mamba state commit into shared spec_utils helpers
- [#28093](https://github.com/sgl-project/sglang/pull/28093) moves draft-extend prep to `EagleDraftWorkerBase` and unifies `prepare_for_*` names
- [#27402](https://github.com/sgl-project/sglang/pull/27402) proactively releases out-of-window SWA slots after chunked prefill
- [#27493](https://github.com/sgl-project/sglang/pull/27493) initializes adaptive spec params from config
- [#28032](https://github.com/sgl-project/sglang/pull/28032) centralizes dummy verify-input capture and adds `carries_draft_hidden_states`
- [#27935](https://github.com/sgl-project/sglang/pull/27935) supports unified_kv_triton for disaggregation on AMD
- [#27764](https://github.com/sgl-project/sglang/pull/27764) extracts move_accept_tokens_to_target_kvcache into spec_utils
- [#24860](https://github.com/sgl-project/sglang/pull/24860) installs `EagleDraftExtendInput` as the V2 draft-extend `spec_info`
- [#27799](https://github.com/sgl-project/sglang/pull/27799) adds `NGRAMWorker` on `BaseSpecWorker` with algo-owned verify-tree shape params
- [#27696](https://github.com/sgl-project/sglang/pull/27696) handles Mooncake buffers across memory release
- [#26288](https://github.com/sgl-project/sglang/pull/26288) supports incremental KV transfer with decode radix cache for AMD
- [#27862](https://github.com/sgl-project/sglang/pull/27862) (opened) supports speculative decoding on CPU
- [#27982](https://github.com/sgl-project/sglang/pull/27982) (opened) adds DraftTailBuffer state machine and CPU tests for decoupled speculative decoding
- [#28010](https://github.com/sgl-project/sglang/pull/28010) (opened) adds DFLASH Mamba/GDN reduced-cache replay
- [#28027](https://github.com/sgl-project/sglang/pull/28027) (opened) adds shared L2 KV cache pool for MLA models (SharedMLA)
- [#28045](https://github.com/sgl-project/sglang/pull/28045) (opened) adds throughput-aware policy for cost-guided adaptive speculative steps
- [#27750](https://github.com/sgl-project/sglang/pull/27750) (opened) extends weight checker to speculative draft workers
- [#27831](https://github.com/sgl-project/sglang/pull/27831) (opened) supports disaggregation-decode-enable-radix-cache and MTP for DeepSeek-V4
- [#27877](https://github.com/sgl-project/sglang/pull/27877) (opened) reuses block KV/req slots in place across FDFO rounds
- [#28185](https://github.com/sgl-project/sglang/pull/28185) (opened) adds int8 checkpoint pool for the linear-attn prefix cache
- [#27886](https://github.com/sgl-project/sglang/pull/27886) (opened) implements feature for weight version isolation in KV cache
- [#28197](https://github.com/sgl-project/sglang/pull/28197) (opened) supports speculative verification for KDA/Kimi-Linear
- [#28104](https://github.com/sgl-project/sglang/pull/28104) (opened) generalizes the DFlash prefill refill heuristic into a bounded PrefillDelayer trigger
- [#27770](https://github.com/sgl-project/sglang/pull/27770) (opened) adds decode-side radix cache for SWA hybrid models
- [#27970](https://github.com/sgl-project/sglang/pull/27970) (opened) adds soft retention priority decay via retention_seconds
- [#28067](https://github.com/sgl-project/sglang/pull/28067) (opened) keeps stop-the-world GC pauses off the batch critical path
- [#27805](https://github.com/sgl-project/sglang/pull/27805) (opened) supports draft KV pool for UnifiedRadixCache for DeepSeek-V4
- [#27979](https://github.com/sgl-project/sglang/pull/27979) (opened) removes CUDA sync between verify(i) and draft(i+1)
- [#27971](https://github.com/sgl-project/sglang/pull/27971) (opened) unifies decode commit accounting to settle kv_committed_len at result time
- [#27998](https://github.com/sgl-project/sglang/pull/27998) (opened) enables speculative decoding (MTP) with radix cache for NemotronH
</details>

<details>
<summary>API & serving (19)</summary>

- [#28071](https://github.com/sgl-project/sglang/pull/28071) enables spatial-shard VAE decode across GPUs
- [#25876](https://github.com/sgl-project/sglang/pull/25876) fixes Anthropic Messages API compatibility
- [#25881](https://github.com/sgl-project/sglang/pull/25881) fixes Responses API request handling
- [#27386](https://github.com/sgl-project/sglang/pull/27386) applies chat template before cache-aware hashing
- [#25954](https://github.com/sgl-project/sglang/pull/25954) adds LRU eviction for mooncacke embedding cache
- [#26670](https://github.com/sgl-project/sglang/pull/26670) adds opt-in LRU eviction to file storage backend
- [#28184](https://github.com/sgl-project/sglang/pull/28184) adds `--warmup-mode` enum for diffusion
- [#27672](https://github.com/sgl-project/sglang/pull/27672) adds bucketed multi-dir layout for NIXL file storage
- [#27875](https://github.com/sgl-project/sglang/pull/27875) enables VAE parallel decode with cfg-parallel
- [#28165](https://github.com/sgl-project/sglang/pull/28165) unifies NVTX annotation helpers and splits the enable gate per subsystem
- [#25994](https://github.com/sgl-project/sglang/pull/25994) adds EPD disaggregated encode tracing
- [#27901](https://github.com/sgl-project/sglang/pull/27901) adds NVTX markers for the scheduler main loop
- [#28158](https://github.com/sgl-project/sglang/pull/28158) (opened) adds compatibility mode for tool parsers
- [#28008](https://github.com/sgl-project/sglang/pull/28008) (opened) adds Anthropic Messages API routing for gateway and PD mode
- [#27778](https://github.com/sgl-project/sglang/pull/27778) (opened) adds repetition truncation logit processor
- [#27921](https://github.com/sgl-project/sglang/pull/27921) (opened) adds load-input-dir feature to replace module inputs from .pt files
- [#28024](https://github.com/sgl-project/sglang/pull/28024) (opened) adds offline file-inject mode to Grafter
- [#27784](https://github.com/sgl-project/sglang/pull/27784) (opened) supports image streaming to OpenAI HTTP server
- [#28004](https://github.com/sgl-project/sglang/pull/28004) (opened) adds OrcaRouter usage example
</details>

<details>
<summary>Hardware & arch (9)</summary>

- [#27811](https://github.com/sgl-project/sglang/pull/27811) restores AMD piecewise CUDA graph support
- [#27857](https://github.com/sgl-project/sglang/pull/27857) shares BCG output buffers across capture sizes with typed ShapeKey
- [#27659](https://github.com/sgl-project/sglang/pull/27659) shares BCG output buffers across capture sizes
- [#27756](https://github.com/sgl-project/sglang/pull/27756) cherry-picks sharing BCG output buffers across capture sizes
- [#27758](https://github.com/sgl-project/sglang/pull/27758) reverts sharing BCG output buffers across capture sizes
- [#27760](https://github.com/sgl-project/sglang/pull/27760) cherry-picks reverting sharing BCG output buffers across capture sizes
- [#27988](https://github.com/sgl-project/sglang/pull/27988) (opened) adds full CUDA graph support for prefill
- [#27746](https://github.com/sgl-project/sglang/pull/27746) (opened) adds a debug tool to detect non-explicitly returned outputs under BCG
- [#28173](https://github.com/sgl-project/sglang/pull/28173) (opened) makes breakable CUDA graph run on ROCm/HIP
</details>

<details>
<summary>Tests (19)</summary>

- [#28127](https://github.com/sgl-project/sglang/pull/28127) improves server warmup coverage for diffusion
- [#28119](https://github.com/sgl-project/sglang/pull/28119) improves diffusion server warmup requests
- [#27102](https://github.com/sgl-project/sglang/pull/27102) evaluates accuracy gpqa aime25 mixins
- [#27913](https://github.com/sgl-project/sglang/pull/27913) adds unit tests for srt/mem_cache/utils.py
- [#27822](https://github.com/sgl-project/sglang/pull/27822) adds label-gated extra-a tier for AMD CI
- [#27710](https://github.com/sgl-project/sglang/pull/27710) adds UT guarding per-request bookkeeping clock ownership
- [#27861](https://github.com/sgl-project/sglang/pull/27861) adds multi-feature and embedding stage-b tests for Intel XPU
- [#27817](https://github.com/sgl-project/sglang/pull/27817) registers 8 attention-backend unit tests to run on AMD CI
- [#25939](https://github.com/sgl-project/sglang/pull/25939) registers 8 framework / unit tests to run on AMD CI
- [#27969](https://github.com/sgl-project/sglang/pull/27969) (opened) adds serving-boundary suite for mixed prefill/decode and agentic-session workloads
- [#27844](https://github.com/sgl-project/sglang/pull/27844) (opened) adds unit tests for srt/parser module
- [#27874](https://github.com/sgl-project/sglang/pull/27874) (opened) adds unit tests for observability/utils, embed_types, mooncake_trace
- [#27996](https://github.com/sgl-project/sglang/pull/27996) (opened) adds unit tests for entrypoints/openai/streaming_asr.py
- [#27731](https://github.com/sgl-project/sglang/pull/27731) (opened) adds runtime per-request bookkeeping clock checks to the invariant checker
- [#27894](https://github.com/sgl-project/sglang/pull/27894) (opened) adds NIXL disaggregation functional tests
- [#28198](https://github.com/sgl-project/sglang/pull/28198) (opened) adds Cohere Command4 detector unit tests
- [#28174](https://github.com/sgl-project/sglang/pull/28174) (opened) adds unit tests for srt/entrypoints/openai/tool_server.py
- [#27934](https://github.com/sgl-project/sglang/pull/27934) (opened) adds unit tests for entrypoints/openai/usage_processor.py
- plus 30+ more minor test updates
</details>

<details>
<summary>CI & build (18)</summary>

- [#26902](https://github.com/sgl-project/sglang/pull/26902) adds Precision Regression Test on Nightly Run CI
- [#26908](https://github.com/sgl-project/sglang/pull/26908) adds unit tests for nixl backend
- [#27149](https://github.com/sgl-project/sglang/pull/27149) adds dsv4 accuracy PR gate to pr-test-amd-rocm720
- [#25007](https://github.com/sgl-project/sglang/pull/25007) adds Arm64 INT8 MoE test coverage
- [#27075](https://github.com/sgl-project/sglang/pull/27075) adds DeepGEMM prerelease wheel tests
- [#27703](https://github.com/sgl-project/sglang/pull/27703) checks out dedicated dir for night build on Intel XPU
- [#27860](https://github.com/sgl-project/sglang/pull/27860) pulls intel/sglang-dev:latest and cleans workspace properly
- [#27795](https://github.com/sgl-project/sglang/pull/27795) removes AMD DSv4 Docker publish job
- [#27766](https://github.com/sgl-project/sglang/pull/27766) removes the legacy release-docs.yml deploy workflow
- [#28108](https://github.com/sgl-project/sglang/pull/28108) enforces modern `stage=`/`runner_config=` form for dispatchable test suites
- [#27648](https://github.com/sgl-project/sglang/pull/27648) cleans build artifacts in cleanup for Intel XPU
- [#27722](https://github.com/sgl-project/sglang/pull/27722) migrates 2-GPU kernel allreduce tests into the registered system for AMD
- [#27133](https://github.com/sgl-project/sglang/pull/27133) updates pytorch-xpu to 2.12
- [#28138](https://github.com/sgl-project/sglang/pull/28138) (opened) adds kernel benchmark regression gate
- [#27765](https://github.com/sgl-project/sglang/pull/27765) (opened) adds amd-miles daily docker build workflow
- [#28089](https://github.com/sgl-project/sglang/pull/28089) (opened) reclaims leaked /dev/shm segments on server startup
- [#28206](https://github.com/sgl-project/sglang/pull/28206) (opened) supports layered overlay images in release-docker-dev
- plus several more minor CI updates
</details>

<details>
<summary>Docs (19)</summary>

- [#27663](https://github.com/sgl-project/sglang/pull/27663) splits NPU best practice docs
- [#28060](https://github.com/sgl-project/sglang/pull/28060) updates docs
- [#28061](https://github.com/sgl-project/sglang/pull/28061) updates docs
- [#27736](https://github.com/sgl-project/sglang/pull/27736) documents progressive resolution growing for Ideogram 4 via GPU DCT upsampling
- [#27767](https://github.com/sgl-project/sglang/pull/27767) updates SGLang-Diffusion docs
- [#27845](https://github.com/sgl-project/sglang/pull/27845) adds cookbook-migrate-model skill from the Qwen3.5 pilot
- [#27677](https://github.com/sgl-project/sglang/pull/27677) replaces `<code>` with backticks and removes obsolete params for NPU docs
- [#27726](https://github.com/sgl-project/sglang/pull/27726) updates MegaMoE handling and reruns benchmarks
- [#27665](https://github.com/sgl-project/sglang/pull/27665) adds mimo best practice
- [#27824](https://github.com/sgl-project/sglang/pull/27824) adds Diffusion Gemma cookbook
- [#27866](https://github.com/sgl-project/sglang/pull/27866) adds Chain-of-Verification (CoVe) hallucination reduction demo
- [#28083](https://github.com/sgl-project/sglang/pull/28083) updates server arguments to NPU support features page
- [#28128](https://github.com/sgl-project/sglang/pull/28128) adds generic config-declared `flagSelects` playground axis
- [#24465](https://github.com/sgl-project/sglang/pull/24465) updates Minimax-M2.5,M2.7 docs with flags for performance
- [#27842](https://github.com/sgl-project/sglang/pull/27842) clarifies that cookbook benchmark accuracy labels come from the model config
- [#28078](https://github.com/sgl-project/sglang/pull/28078) adds llm-d page under Advanced Features
- [#27893](https://github.com/sgl-project/sglang/pull/27893) (opened) creates deployment tutorials for mainstream models on Ascend NPU
- [#27848](https://github.com/sgl-project/sglang/pull/27848) (opened) migrates Qwen3.5 cookbook to the config-driven template
- [#28159](https://github.com/sgl-project/sglang/pull/28159) (opened) migrates Kimi-K2.6 to the config-driven template
</details>

<details>
<summary>Bugfixes (21)</summary>

- [#23862](https://github.com/sgl-project/sglang/pull/23862) fixes `--mem-fraction-static` not accounting for EAGLE draft model KV cache
- [#27529](https://github.com/sgl-project/sglang/pull/27529) fixes DeepSeek V4 Pro c128 state tensor dtype mismatch error
- [#27919](https://github.com/sgl-project/sglang/pull/27919) reverts DeepSeek V4 Pro c128 state tensor dtype mismatch error fix
- [#27808](https://github.com/sgl-project/sglang/pull/27808) fixes NPU MTP graph runner
- [#27655](https://github.com/sgl-project/sglang/pull/27655) fixes compatibility bugs with eagle and unified l3
- [#27737](https://github.com/sgl-project/sglang/pull/27737) fixes flashinfer swa kv pool for dflash gemma 4
- [#28022](https://github.com/sgl-project/sglang/pull/28022) fixes resource leak on prealloc/transfer abort and idle check
- [#27876](https://github.com/sgl-project/sglang/pull/27876) fixes Wan TI2V SP timestep padding
- [#28088](https://github.com/sgl-project/sglang/pull/28088) fixes frontend returning HTTP 400 for out-of-vocabulary token_ids_logprob
- [#27883](https://github.com/sgl-project/sglang/pull/27883) fixes fp16 NaN flake in spec CI and sanitizes NaN logits in sampler
- [#26351](https://github.com/sgl-project/sglang/pull/26351) commits Mamba states after NGRAM target verify
- [#28096](https://github.com/sgl-project/sglang/pull/28096) fixes EagleDraftWorker draft-extend attn backend assignment
- [#27840](https://github.com/sgl-project/sglang/pull/27840) uses int64 seq_lens across all CUDA graph runners and backends
- [#27190](https://github.com/sgl-project/sglang/pull/27190) emulates PDEATHSIG on macOS to prevent orphaned worker processes
- [#26971](https://github.com/sgl-project/sglang/pull/26971) indexes extra_key per sub-request in batched GenerateReqInput
- [#27869](https://github.com/sgl-project/sglang/pull/27869) fixes Qwen3.5 deterministic batch-invariant logprobs
- [#26203](https://github.com/sgl-project/sglang/pull/26203) fixes MLA scaling when YARN scaling is disabled
- [#27796](https://github.com/sgl-project/sglang/pull/27796) fixes ZMQ stale socket reconnection in PD disaggregation
- [#27608](https://github.com/sgl-project/sglang/pull/27608) fixes prefill bootstrap registration failure with `--host 0.0.0.0`
- [#27039](https://github.com/sgl-project/sglang/pull/27039) fixes zmq PUSH socket reconnect-aware connection management
- plus 60 more minor bugfixes
</details>

<details>
<summary>Refactors (11)</summary>

- [#27698](https://github.com/sgl-project/sglang/pull/27698) refactors realtime control state and adapters for diffusion
- [#26678](https://github.com/sgl-project/sglang/pull/26678) moves HiSparse allocators to allocator/hisparse.py
- [#27984](https://github.com/sgl-project/sglang/pull/27984) enables Ruff UP037 to drop redundant quoted annotations
- [#27697](https://github.com/sgl-project/sglang/pull/27697) refactors realtime and model-specific stage modules for diffusion
- [#28107](https://github.com/sgl-project/sglang/pull/28107) follows up on CUDA Graph refactor code style
- [#27761](https://github.com/sgl-project/sglang/pull/27761) removes dead `prepare_for_verify` / `prepare_extend_after_decode` and extend-decode kernel
- [#28081](https://github.com/sgl-project/sglang/pull/28081) folds FrozenKVMTPCudaGraphRunner onto the shared DecodeCudaGraphRunner base
- [#28211](https://github.com/sgl-project/sglang/pull/28211) (opened) centralizes FlashInfer CUTLASS MoE runner
- [#28001](https://github.com/sgl-project/sglang/pull/28001) (opened) refactors weight processing in RL weight update
- [#28151](https://github.com/sgl-project/sglang/pull/28151) (opened) refactors mamba radix cache server args initialization
- [#28069](https://github.com/sgl-project/sglang/pull/28069) (opened) adds torch_native MoE runner backend
</details>

<details>
<summary>Other (33)</summary>

- [#28117](https://github.com/sgl-project/sglang/pull/28117) moves eagle verify `prepare_for_verify`/`sample` to `eagle_utils` free helpers
- [#27847](https://github.com/sgl-project/sglang/pull/27847) cherry-picks disabling async assert in Nemotron nightly tests
- [#28177](https://github.com/sgl-project/sglang/pull/28177) resolves model_index.json Hub-first with local-cache fallback
- [#27865](https://github.com/sgl-project/sglang/pull/27865) cherry-picks fixing UnifiedRadixCache write-back load_back / eviction crashes
- [#27743](https://github.com/sgl-project/sglang/pull/27743) cherry-picks fixing flaky hicache l3 mmlu nightly test
- [#27994](https://github.com/sgl-project/sglang/pull/27994) removes outdated patch
- [#27841](https://github.com/sgl-project/sglang/pull/27841) removes MoE prefill CUDA graph disable guard
- [#27307](https://github.com/sgl-project/sglang/pull/27307) converts DeepSeek V4 APE layout through weight loader
- [#28193](https://github.com/sgl-project/sglang/pull/28193) uses regional torch.compile for DiT
- [#27895](https://github.com/sgl-project/sglang/pull/27895) (opened) introduces RuntimeContext for consolidating process-level global state
- [#28162](https://github.com/sgl-project/sglang/pull/28162) (opened) allows custom spec algorithm to handle server args
- [#27741](https://github.com/sgl-project/sglang/pull/27741) (opened) merges Pcg npu for qwen3, qwen3.5, and dsv2-lite
- [#28082](https://github.com/sgl-project/sglang/pull/28082) (opened) adds ULP-based quant error tolerance via allow_quant_error
- [#28086](https://github.com/sgl-project/sglang/pull/28086) (opened) aborts during chunked prefill and PD peer-liveness abort
- [#27980](https://github.com/sgl-project/sglang/pull/27980) (opened) reconciles workers that registered without resolving model_ids
- [#27990](https://github.com/sgl-project/sglang/pull/27990) (opened) updates pp
- [#27834](https://github.com/sgl-project/sglang/pull/27834) (opened) routes collectives through torchcomms
- [#27989](https://github.com/sgl-project/sglang/pull/27989) (opened) runs tests locally
- [#28113](https://github.com/sgl-project/sglang/pull/28113) (opened) routes pin memory availability through current_platform
- [#28068](https://github.com/sgl-project/sglang/pull/28068) (opened) makes RadixCache.evict free pages without device syncs
- [#28161](https://github.com/sgl-project/sglang/pull/28161) (opened) wires SGLANG_OPT_SWA_RELEASE_LEAF_LOCK_AFTER_WINDOW on Unified Cache
- [#28065](https://github.com/sgl-project/sglang/pull/28065) (opened) optimizes Lingbot World
- [#27929](https://github.com/sgl-project/sglang/pull/27929) (opened) adds VAE NHWC for Lingbot World
- [#27755](https://github.com/sgl-project/sglang/pull/27755) (opened) updates LingBot-World chunk-size through webui
- [#27954](https://github.com/sgl-project/sglang/pull/27954) (opened) pads MLA decode q-heads to 64 for FlashMLA head64 kernel
- [#27918](https://github.com/sgl-project/sglang/pull/27918) (opened) restores Qwen3.5 MRoPE fusion under breakable CUDA graph
- [#27729](https://github.com/sgl-project/sglang/pull/27729) (opened) warms DeepGEMM MHC prenorm split buckets
- [#27986](https://github.com/sgl-project/sglang/pull/27986) (opened) prewarms MHC prenorm kernel at startup
- [#28204](https://github.com/sgl-project/sglang/pull/28204) (opened) optimizes causal Conv3d VAE padding
- [#28205](https://github.com/sgl-project/sglang/pull/28205) (opened) persists torch.compile Inductor/Triton cache across restarts
- [#27791](https://github.com/sgl-project/sglang/pull/27791) (opened) avoids syncing non-MTP weights to Qwen3.5 MTP draft runner
- [#28053](https://github.com/sgl-project/sglang/pull/28053) (opened) disables dsr1 prefill cudagraphs by default
- [#28085](https://github.com/sgl-project/sglang/pull/28085) (opened) optimizes SWA allocation
</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (sglang.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
