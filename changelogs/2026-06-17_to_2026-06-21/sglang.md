# sglang: PR digest (2026-06-17 to 2026-06-21)

_200 merged, 204 newly opened - source sgl-project/sglang, generated 2026-06-21T22:31:08Z_

## TL;DR
- **Model focus:** DeepSeek (V4 NPU support, mixed dtype compression), MiniMax (massive in-progress PRs for M3 support including sparse attention and FP8), GLM, and Qwen.
- **Performance & Architecture:** Major refactoring of parallel topology state via `get_parallel()`, introduction of a Rust-based Unified Radix Cache (in design), and layer-pipeline disaggregation work.
- **Kernels & Attention:** Significant Triton and FlashInfer kernel updates, including split-KV flash-decode for EAGLE on AMD, and double sparsity v2 in progress.
- **Multimodal & Diffusion:** Megatron-style Tensor Parallelism added for native encoders and DiTs, plus continuous batching for diffusion models in progress.
- **Overall Direction:** Heavy investment in scaling out (disaggregation, layer pipelines, Rust radix cache) and optimizing for specific hardware (AMD ROCm, Ascend NPU) alongside deep optimizations for DeepSeek-V4 and MiniMax-M3.

## Most important PRs
- **[#28712](https://github.com/sgl-project/sglang/pull/28712)** (and related [#28715](https://github.com/sgl-project/sglang/pull/28715), [#28713](https://github.com/sgl-project/sglang/pull/28713), [#28714](https://github.com/sgl-project/sglang/pull/28714)): **Newly opened: MiniMax-M3 support.** A massive multi-part PR series introducing sparse attention ops, JIT kernels, FP8 quantization, and disaggregated K-only index-K transfer for the MiniMax-M3 model.
- **[#28567](https://github.com/sgl-project/sglang/pull/28567)** (and [#28568](https://github.com/sgl-project/sglang/pull/28568)): **Add `get_parallel()` accessor.** Replaces ad-hoc parallel dimension handling with a structured accessor for parallel-topology state, standardizing the model forward path across backends.
- **[#28529](https://github.com/sgl-project/sglang/pull/28529)**: **Newly opened: Disaggregated layer pipeline.** Introduces a layer pipeline architecture for disaggregated serving, significantly expanding distributed inference capabilities.
- **[#28701](https://github.com/sgl-project/sglang/pull/28701)**: **Newly opened: Rust Unified Radix Cache.** A major design proposal and implementation to rewrite the radix cache in Rust for improved performance and safety.
- **[#25144](https://github.com/sgl-project/sglang/pull/25144)**: **Ascend NPU support for DeepSeek-V4.** Adds comprehensive support for DeepSeek-V4 on Ascend NPUs, including attention, kernels, MoE, and speculative decoding.

## More changes by area

<details>
<summary>Performance (17)</summary>

- [#27066](https://github.com/sgl-project/sglang/pull/27066) Shard text when using SP in FLUX.1/2
- [#28594](https://github.com/sgl-project/sglang/pull/28594) Merge LTX-2 stage-1 distilled LoRA into the base
- [#28722](https://github.com/sgl-project/sglang/pull/28722) Optimize o_proj gemm and attn output rope performance on AMD
- [#22445](https://github.com/sgl-project/sglang/pull/22445) Performance optimization for LTX-2 model on NPU
- [#28500](https://github.com/sgl-project/sglang/pull/28500) Make spec-decode penalty H2D non-blocking
- [#28491](https://github.com/sgl-project/sglang/pull/28491) Make latest_output_ids H2D non-blocking in prepare_for_decode
- [#27793](https://github.com/sgl-project/sglang/pull/27793) Tune extend attention block sizes for gfx950
- [#28844](https://github.com/sgl-project/sglang/pull/28844) Fuse QK RMSNorm + RoPE into single Triton op for Qwen3.5-397B on HIP
- [#28756](https://github.com/sgl-project/sglang/pull/28756) Shard cache-aware-zmq radix tree to remove read-vs-write lock contention
- [#28476](https://github.com/sgl-project/sglang/pull/28476) Fuse QK-norm + 3D mRoPE + KV cache store into single aiter op for Qwen3.5 on HIP
- [#28700](https://github.com/sgl-project/sglang/pull/28700) Fuse QK RMSNorm + 3D mRoPE + KV-cache store into single aiter op for Qwen3.5 on HIP
- [#28624](https://github.com/sgl-project/sglang/pull/28624) Optimize LTX2.3 CFG/SP paths
- [#28780](https://github.com/sgl-project/sglang/pull/28780) Optimize DMD Wan auto residency on high-memory GPUs
- [#28527](https://github.com/sgl-project/sglang/pull/28527) Add optimizations for CPU platform diffusion
- [#28672](https://github.com/sgl-project/sglang/pull/28672) Skip custom all-reduce v2 CUDA graph capture with torch memory saver
- [#28729](https://github.com/sgl-project/sglang/pull/28729) Offload fp8 wo_a dequant to GPU to speed up weight loading for DeepSeek-V4
- [#28783](https://github.com/sgl-project/sglang/pull/28783) Optimize rope triton kernel performance for v4 model on AMD

</details>

<details>
<summary>Kernels & attention (25)</summary>

- [#27382](https://github.com/sgl-project/sglang/pull/27382) Split-KV flash-decode attention for EAGLE target-verify on AMD
- [#28185](https://github.com/sgl-project/sglang/pull/28185) Int8 checkpoint pool for the linear-attn prefix cache
- [#28106](https://github.com/sgl-project/sglang/pull/28106) Make seq_lens_cpu optional in trtllm_mha backend
- [#28302](https://github.com/sgl-project/sglang/pull/28302) Deduplicate spec conv-window intermediate cache via sliding window layout
- [#28346](https://github.com/sgl-project/sglang/pull/28346) Use Flashinfer allreduce fusion for MNNVL allreduce for Nemotron
- [#28393](https://github.com/sgl-project/sglang/pull/28393) Pack self-attn q/k/v and cross-attn k/v into single GEMMs for Sana
- [#28579](https://github.com/sgl-project/sglang/pull/28579) Fully overlap spec decoding for hybrid linear attention backend
- [#25702](https://github.com/sgl-project/sglang/pull/25702) Use pack topk ids triton kernel for flashinfer_trtllm_routed
- [#25768](https://github.com/sgl-project/sglang/pull/25768) Replace ascend vision attn operator on NPU
- [#28436](https://github.com/sgl-project/sglang/pull/28436) Use use_dsa to dispatch Ascend DSA attention
- [#28642](https://github.com/sgl-project/sglang/pull/28642) Add lost params in fa varlen func
- [#28709](https://github.com/sgl-project/sglang/pull/28709) Double sparsity v2
- [#28639](https://github.com/sgl-project/sglang/pull/28639) Add ag_gemm and moe_rs overlap kernels for dsv4 prefill
- [#28716](https://github.com/sgl-project/sglang/pull/28716) XPU jit kernel support
- [#28670](https://github.com/sgl-project/sglang/pull/28670) Add kpool_topk_transform JIT kernel
- [#28637](https://github.com/sgl-project/sglang/pull/28637) Support head_dim=80 via padding for flash attention SYCL kernel on XPU
- [#28789](https://github.com/sgl-project/sglang/pull/28789) Re-enable SM90 FlashInfer allreduce fusion with safe backend defaults
- [#28655](https://github.com/sgl-project/sglang/pull/28655) GDN linear out proj fusion on AMD
- [#28570](https://github.com/sgl-project/sglang/pull/28570) Support bf16 KV cache in tokenspeed_mla
- [#28686](https://github.com/sgl-project/sglang/pull/28686) Enable prefill piecewise CUDA graph for Cohere2Vision text path
- [#28842](https://github.com/sgl-project/sglang/pull/28842) Support TBO prefill-only mode on single machine
- [#28482](https://github.com/sgl-project/sglang/pull/28482) Contiguous varlen FMHA for Qwen3.5 mxfp4 on AMD
- [#28723](https://github.com/sgl-project/sglang/pull/28723) Support fused_moe_triton kernel tuning on Intel XPU
- [#28757](https://github.com/sgl-project/sglang/pull/28757) Skip redundant -inf pre-fill of HIP indexer MQA-logits for GLM5
- [#28542](https://github.com/sgl-project/sglang/pull/28542) Minor attention update for NPU

</details>

<details>
<summary>MoE & quantization (22)</summary>

- [#28231](https://github.com/sgl-project/sglang/pull/28231) Use Marlin for SM120 MXFP4 MoE
- [#28505](https://github.com/sgl-project/sglang/pull/28505) Delegate MXFP8 dense scheme to kernel and use torch.ops.npu
- [#28216](https://github.com/sgl-project/sglang/pull/28216) DP MoE reduce scatter on AMD
- [#26766](https://github.com/sgl-project/sglang/pull/26766) Fuse UE8M0 scale rounding into FP8 group quantization for DeepSeek-V4
- [#28333](https://github.com/sgl-project/sglang/pull/28333) Call Flashinfer mm_fp8 for per-tensor FP8 GEMMs on SM100
- [#27690](https://github.com/sgl-project/sglang/pull/27690) Support asymmetric compressed-tensors MoE
- [#28555](https://github.com/sgl-project/sglang/pull/28555) Remove redundant cast and copy in calling trtllm_fp8_block_scale_moe
- [#28649](https://github.com/sgl-project/sglang/pull/28649) Pass quant_config to attention gate projection
- [#28552](https://github.com/sgl-project/sglang/pull/28552) Add Triton block-FP8 GEMM tuned configs for Qwen3.5 on Blackwell SM120
- [#28735](https://github.com/sgl-project/sglang/pull/28735) Add ScaleSweep MSE NVFP4 activation quantization
- [#28574](https://github.com/sgl-project/sglang/pull/28574) Fuse deferred MoE finalize into next-layer AR + residual + RMSNorm for Kimi K2.5
- [#28620](https://github.com/sgl-project/sglang/pull/28620) Add SM89 FP8 indexer fallback for DeepSeek V4 Flash
- [#28564](https://github.com/sgl-project/sglang/pull/28564) Extend virtual-experts kernel for gate_up fusion and tighten MoE LoRA path
- [#28666](https://github.com/sgl-project/sglang/pull/28666) Fuse shared_expert_gate GEMV into the MoE append kernel on AMD
- [#28703](https://github.com/sgl-project/sglang/pull/28703) DSA indexer LoRA targets for GLM-5.1 / DeepSeek-V3.2-family
- [#28689](https://github.com/sgl-project/sglang/pull/28689) Dedup triton_kernels backend quant-arg asserts and fill weight dtype guard
- [#28658](https://github.com/sgl-project/sglang/pull/28658) Fuse shared-expert sigmoid + bf16->fp32 cast into the MoE append kernel on AMD
- [#28562](https://github.com/sgl-project/sglang/pull/28562) Per-rank serialization for load_lora_adapter_from_tensors
- [#28676](https://github.com/sgl-project/sglang/pull/28676) MXFP8 flashinfer_trtllm_routed MoE for V4
- [#28566](https://github.com/sgl-project/sglang/pull/28566) Sentinel-pad token->lora mapping for DP-attention foreign tokens
- [#28786](https://github.com/sgl-project/sglang/pull/28786) Enable FlashInfer allreduce for Qwen3-VL MoE on B300
- [#28526](https://github.com/sgl-project/sglang/pull/28526) Quantize bfloat16 hidden_states before npu_grouped_matmul in W4 on NPU

</details>

<details>
<summary>Model support (16)</summary>

- [#27277](https://github.com/sgl-project/sglang/pull/27277) Support mixed dtype compression states for Deepseek v4
- [#28661](https://github.com/sgl-project/sglang/pull/28661) Add Laguna-M.1 cookbook
- [#27471](https://github.com/sgl-project/sglang/pull/27471) Add dflash gemma4 support
- [#28664](https://github.com/sgl-project/sglang/pull/28664) Enable FP8 on Blackwell for Laguna-M.1
- [#28737](https://github.com/sgl-project/sglang/pull/28737) Add PD disaggregation section for Laguna-M.1
- [#28176](https://github.com/sgl-project/sglang/pull/28176) Use LocalAttention for Mistral3 encoder
- [#28400](https://github.com/sgl-project/sglang/pull/28400) Support per-element output gating for Laguna
- [#28516](https://github.com/sgl-project/sglang/pull/28516) Add MTP support for GLM-4.7-Flash on NPU
- [#28635](https://github.com/sgl-project/sglang/pull/28635) Add head_dim=256 to _can_use_tnd whitelist on NPU
- [#28671](https://github.com/sgl-project/sglang/pull/28671) AutoWeightLoader support Sglang native models
- [#28691](https://github.com/sgl-project/sglang/pull/28691) Add LFM2.5 embedding model support
- [#28506](https://github.com/sgl-project/sglang/pull/28506) Add InstantTensor model weight loader
- [#28557](https://github.com/sgl-project/sglang/pull/28557) Add Qwen-Image ModelOpt NVFP4 support
- [#28773](https://github.com/sgl-project/sglang/pull/28773) Keep FastHunyuan VAE resident on high-memory GPUs
- [#28675](https://github.com/sgl-project/sglang/pull/28675) Add mamba-backend and SSM dtype flags for Nemotron3-Ultra
- [#28727](https://github.com/sgl-project/sglang/pull/28727) Support bf16 dtype for Ideogram

</details>

<details>
<summary>Parallelism & scheduling (37)</summary>

- [#28434](https://github.com/sgl-project/sglang/pull/28434) Support hybrid pool staged H2D kernel for HiCache
- [#28318](https://github.com/sgl-project/sglang/pull/28318) Use Megatron-style TP for native encoders and DiTs
- [#28421](https://github.com/sgl-project/sglang/pull/28421) Implement zigzag CP strategy
- [#28086](https://github.com/sgl-project/sglang/pull/28086) Abort during chunked prefill + PD peer-liveness abort
- [#26312](https://github.com/sgl-project/sglang/pull/26312) Add rejection sampling for speculative decoding
- [#28682](https://github.com/sgl-project/sglang/pull/28682) Unify speculative grammar token-accept path in decode processing
- [#28575](https://github.com/sgl-project/sglang/pull/28575) Revert mtp update weight from distributed
- [#28755](https://github.com/sgl-project/sglang/pull/28755) Cap SWA pool sizing with chunk cache
- [#28161](https://github.com/sgl-project/sglang/pull/28161) Wire SWA release leaf lock after window on Unified Cache
- [#28683](https://github.com/sgl-project/sglang/pull/28683) Split init_backends and account draft weights in mem-fraction-static
- [#28841](https://github.com/sgl-project/sglang/pull/28841) Revert split init_backends
- [#28465](https://github.com/sgl-project/sglang/pull/28465) Batch EAGLE draft/draft-extend replay memcpys via grouped foreach copy
- [#28782](https://github.com/sgl-project/sglang/pull/28782) Support FlashInfer CUDA graph for EAGLE draft-extend
- [#28162](https://github.com/sgl-project/sglang/pull/28162) Custom spec algorithm can handle server args
- [#28779](https://github.com/sgl-project/sglang/pull/28779) Add graceful scheduler shutdown and free hisparse host buffer on exit
- [#28319](https://github.com/sgl-project/sglang/pull/28319) Shard HunyuanVideo text tokens under SP
- [#28785](https://github.com/sgl-project/sglang/pull/28785) Pass DSA topk through PP warmup proxy buffers
- [#28408](https://github.com/sgl-project/sglang/pull/28408) Remove stale load collection from output streaming hot path
- [#28690](https://github.com/sgl-project/sglang/pull/28690) Continuous batching v0 for diffusion
- [#28538](https://github.com/sgl-project/sglang/pull/28538) Support deepseek v4 decode context parallel based on unified kv attention backend
- [#28523](https://github.com/sgl-project/sglang/pull/28523) Support IndexCache shared layer IO overlap for HiSparse
- [#28695](https://github.com/sgl-project/sglang/pull/28695) Support ReplaySSM Ring Spec-Verify for GDN
- [#28515](https://github.com/sgl-project/sglang/pull/28515) Decoding-to-Prefilling (D2P) KV Transfer for PD Disagg
- [#28612](https://github.com/sgl-project/sglang/pull/28612) Optimize C128 state pool allocation using request state pool
- [#28608](https://github.com/sgl-project/sglang/pull/28608) Prefix KV Cache Pinning for RL Rollout
- [#28680](https://github.com/sgl-project/sglang/pull/28680) Support grammar constrained decoding support for DFlash
- [#28775](https://github.com/sgl-project/sglang/pull/28775) Concentrate CP communication ownership in communicator
- [#28477](https://github.com/sgl-project/sglang/pull/28477) Add SLA-constrained dynamic batching for decode phase optimization
- [#28855](https://github.com/sgl-project/sglang/pull/28855) Redo split init_backends and account draft weights
- [#28654](https://github.com/sgl-project/sglang/pull/28654) Shard HiCache file backend into hash-prefix subdirs
- [#28614](https://github.com/sgl-project/sglang/pull/28614) Remove large host mem constraint for HiCache
- [#28854](https://github.com/sgl-project/sglang/pull/28854) Add sync-free fast_prefill_plan for EAGLE draft-extend CUDA graph
- [#28616](https://github.com/sgl-project/sglang/pull/28616) Support NGRAM speculative decoding with DP attention
- [#28843](https://github.com/sgl-project/sglang/pull/28843) Fine-grained overlap-schedule WAR barrier via metadata-read-done event
- [#28651](https://github.com/sgl-project/sglang/pull/28651) Notify decode peer when a prefill request is aborted for disaggregation
- [#28856](https://github.com/sgl-project/sglang/pull/28856) Enable FR-Spec in EAGLE draft-extend CUDA graph
- [#28504](https://github.com/sgl-project/sglang/pull/28504) Skip empty non-idle output batches

</details>

<details>
<summary>Hardware & arch (4)</summary>

- [#26639](https://github.com/sgl-project/sglang/pull/26639) Enable HiSparse on ROCm
- [#26385](https://github.com/sgl-project/sglang/pull/26385) Introduce CpuDeviceMixin and CpuSRTPlatform
- [#28173](https://github.com/sgl-project/sglang/pull/28173) Make breakable CUDA graph run on ROCm/HIP
- [#28473](https://github.com/sgl-project/sglang/pull/28473) Fall back to layer_first layout for kernel write-back on ROCm

</details>

<details>
<summary>API & serving (19)</summary>

- [#28744](https://github.com/sgl-project/sglang/pull/28744) Tokenize prompt once at ingress and forward input_ids to the engine
- [#26252](https://github.com/sgl-project/sglang/pull/26252) Add Ray metric backend wrappers
- [#28122](https://github.com/sgl-project/sglang/pull/28122) Add Metal profiling hooks to server profiler
- [#28573](https://github.com/sgl-project/sglang/pull/28573) Support MPServer and embedded server for granian
- [#22053](https://github.com/sgl-project/sglang/pull/22053) Add cache hit breakdown in bench_serving
- [#28551](https://github.com/sgl-project/sglang/pull/28551) Add opt-in CUDA-graph capture-trace export
- [#28742](https://github.com/sgl-project/sglang/pull/28742) Raise chat body cap to 5 MiB for long contexts
- [#28717](https://github.com/sgl-project/sglang/pull/28717) Align sgl_router_ttft_seconds buckets with engine TTFT grid
- [#28807](https://github.com/sgl-project/sglang/pull/28807) Clean up startup log noise
- [#28600](https://github.com/sgl-project/sglang/pull/28600) Load-aware selection from engine LoadStat for cache_aware_zmq router
- [#28599](https://github.com/sgl-project/sglang/pull/28599) Publish per-scheduler load on a dedicated socket for load-aware routers
- [#28509](https://github.com/sgl-project/sglang/pull/28509) Add decision-level observability to the cache-aware routing policy
- [#28497](https://github.com/sgl-project/sglang/pull/28497) Add language-model-only flag to skip multimodal encoder loading
- [#28470](https://github.com/sgl-project/sglang/pull/28470) Add scheduler prefill queue wait breakdown
- [#28507](https://github.com/sgl-project/sglang/pull/28507) Add cache eviction lifetime/frequency metrics
- [#28720](https://github.com/sgl-project/sglang/pull/28720) Add tokenization hot-path benchmark
- [#28822](https://github.com/sgl-project/sglang/pull/28822) Add system_fingerprint to Python OpenAI chat/completion responses
- [#28510](https://github.com/sgl-project/sglang/pull/28510) Add a per-request cache-match snapshot
- [#28508](https://github.com/sgl-project/sglang/pull/28508) Export radix cache size gauges

</details>

<details>
<summary>Tests, CI & build (73)</summary>

- [#28810](https://github.com/sgl-project/sglang/pull/28810) Remove deprecated test/srt legacy CI setup
- [#28536](https://github.com/sgl-project/sglang/pull/28536) Run GB300 nightly suite in the standard Nvidia nightly workflow
- [#28811](https://github.com/sgl-project/sglang/pull/28811) Sort pyproject dependency lists
- [#28607](https://github.com/sgl-project/sglang/pull/28607) Drop redundant req_pool_indices_cpu guards and fold hisparse into GLM-5.1 e2e
- [#28625](https://github.com/sgl-project/sglang/pull/28625) Move bench_one_batch_server into sglang/benchmark/
- [#28592](https://github.com/sgl-project/sglang/pull/28592) Centralize bench launch-vs-connect into a reusable acquire_endpoint
- [#28577](https://github.com/sgl-project/sglang/pull/28577) Fold EAGLE return_hidden_states regression into spec triton suite
- [#28745](https://github.com/sgl-project/sglang/pull/28745) Add 4-GPU mi35x runner and rebalance off the saturated 8-GPU pool
- [#28751](https://github.com/sgl-project/sglang/pull/28751) Revert 4-GPU mi35x runner
- [#28598](https://github.com/sgl-project/sglang/pull/28598) Share bench HTTP-client base-URL resolution with IPv6-compatible formatting
- plus 63 more minor CI and test updates

</details>

<details>
<summary>Docs (30)</summary>

- [#28423](https://github.com/sgl-project/sglang/pull/28423) Update v4 amd cookbook
- [#28533](https://github.com/sgl-project/sglang/pull/28533) Remove ltx2 snapshot mode
- [#28697](https://github.com/sgl-project/sglang/pull/28697) Add B300 cookbook deployment options
- [#28433](https://github.com/sgl-project/sglang/pull/28433) GLM 5.2 deployment on Ascend
- [#28719](https://github.com/sgl-project/sglang/pull/28719) Remove outdated SGLang SOTA skill
- plus 25 more minor documentation updates

</details>

<details>
<summary>Bugfixes (93)</summary>

- [#28371](https://github.com/sgl-project/sglang/pull/28371) Fix chunked SGMV CUDA graph segment replay
- [#28499](https://github.com/sgl-project/sglang/pull/28499) Fix chunked SGMV CUDA graph segment replay
- [#24082](https://github.com/sgl-project/sglang/pull/24082) Fix spec decoding with grammar in disagg
- [#24970](https://github.com/sgl-project/sglang/pull/24970) Fix Step3-VL multi-image embedding and local patch splitting
- [#28091](https://github.com/sgl-project/sglang/pull/28091) Fix experimental fast-path multi-adapter correctness
- [#28244](https://github.com/sgl-project/sglang/pull/28244) Fix garbled unquantized Qwen3-30B-A3B output on ROCm/aiter
- [#28520](https://github.com/sgl-project/sglang/pull/28520) Fix deepseek-v4 mtp accept length issue on AMD
- [#28694](https://github.com/sgl-project/sglang/pull/28694) Fix tokenizer state cleanup on dispatch failure
- [#26773](https://github.com/sgl-project/sglang/pull/26773) Handle mid-conversation system messages for Anthropic
- [#28074](https://github.com/sgl-project/sglang/pull/28074) Fix no-op dtype cast in _topk_ids_logical_to_physical_dynamic on HIP
- plus 83 more minor bugfixes

</details>

<details>
<summary>Refactors (25)</summary>

- [#28739](https://github.com/sgl-project/sglang/pull/28739) Move kernel warmup into the shared runner lifecycle
- [#28386](https://github.com/sgl-project/sglang/pull/28386) Add EagerRunner, own the eager path, polymorphic dispatch
- [#27273](https://github.com/sgl-project/sglang/pull/27273) Extract host KV cache base layer into pool_host package
- [#28814](https://github.com/sgl-project/sglang/pull/28814) Auto-derive CLI args from dataclass fields to eliminate duplication
- [#28548](https://github.com/sgl-project/sglang/pull/28548) Centralize speculative weight-update fan-out in the scheduler
- [#28740](https://github.com/sgl-project/sglang/pull/28740) Reuse a prepared static buffer for every dummy run
- [#28710](https://github.com/sgl-project/sglang/pull/28710) Unify RL weight-update fanout across target and draft/MTP
- [#28151](https://github.com/sgl-project/sglang/pull/28151) Mamba radix cache server args initialize
- [#28833](https://github.com/sgl-project/sglang/pull/28833) Bound DiffGenerator local cleanup
- [#28384](https://github.com/sgl-project/sglang/pull/28384) Rename runner replay/load/can_run for the shared surface
- [#28385](https://github.com/sgl-project/sglang/pull/28385) Split BaseRunner (shared) from BaseCudaGraphRunner
- [#26003](https://github.com/sgl-project/sglang/pull/26003) Remove unused transfer buffer in HiCache
- [#28383](https://github.com/sgl-project/sglang/pull/28383) Unify eager-forward DP/MLP-sync padding into one helper
- [#28576](https://github.com/sgl-project/sglang/pull/28576) Unify bench seed default to 42 and rename profile-filename-prefix
- [#28382](https://github.com/sgl-project/sglang/pull/28382) Unify pp_proxy_tensors forward kwarg into one helper
- [#28765](https://github.com/sgl-project/sglang/pull/28765) Converge metadata bodies into _compute_forward_metadata per backend
- [#28688](https://github.com/sgl-project/sglang/pull/28688) Migrate from pickle to msgpack
- [#28767](https://github.com/sgl-project/sglang/pull/28767) Deprecate use_bound parameter on _compute_forward_metadata
- [#28492](https://github.com/sgl-project/sglang/pull/28492) Simplify MultiLayerEagleDraftExtendCudaGraphRunner to use rotation
- [#28830](https://github.com/sgl-project/sglang/pull/28830) Migrate more server args to annotated style
- [#28609](https://github.com/sgl-project/sglang/pull/28609) Refactor index topk sharing policy
- [#28763](https://github.com/sgl-project/sglang/pull/28763) Rename init_cuda_graph_state -> init_static_metadata_buffers
- [#28494](https://github.com/sgl-project/sglang/pull/28494) Decouple allocator runtime from KV pool
- [#28764](https://github.com/sgl-project/sglang/pull/28764) Allocate attention static metadata buffers at eager init
- [#28766](https://github.com/sgl-project/sglang/pull/28766) Route eager metadata init through out_graph

</details>

<details>
<summary>Other (7)</summary>

- [#28708](https://github.com/sgl-project/sglang/pull/28708) Revert FLUX fuse FeedForward GELU into up-proj GEMM
- [#28571](https://github.com/sgl-project/sglang/pull/28571) Revert the head_dim assignment from PR 23862
- [#28583](https://github.com/sgl-project/sglang/pull/28583) Revert revert the head_dim assignment from PR 23862
- [#28812](https://github.com/sgl-project/sglang/pull/28812) Remove threading atexit monkey patch
- [#28561](https://github.com/sgl-project/sglang/pull/28561) Revert deepseek_weight_loader.py changes
- [#28524](https://github.com/sgl-project/sglang/pull/28524) Trainer ft/dev
- [#28591](https://github.com/sgl-project/sglang/pull/28591) Revert DeepSeek-V4 Online Compress support MTP

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (sglang.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
