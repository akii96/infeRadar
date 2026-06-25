# vllm: PR digest (2026-06-21 to 2026-06-25)

_215 merged, 243 newly opened - source vllm-project/vllm, generated 2026-06-25T11:49:50Z_

## TL;DR
- **DeepSeek** models received the most attention, with merged support for DeepSeek V4 on Blackwell (SM120) and a new cluster-cooperative topK kernel for low-latency MoE routing.
- **Performance & Kernels** saw major memory wins with merged Triton INT4 per-token-head KV cache quantization, alongside newly opened work on HiSparse MLA decode and FlashAttention prefill-context-parallel (PCP) for GQA.
- **Hardware & Architecture** expanded with newly opened support for the RWKV7 Albatross architecture, initial enablement for AMD's gfx1250 ROCm architecture, and Blackwell NVFP4 KV cache optimizations for Gemma 3/4.
- **Frontend & Serving** underwent a major refactor with the merged introduction of a unified parser interface in the Rust frontend, plus newly opened streaming parser engines and TLS support.
- **Distributed & Disaggregation** is advancing toward robust disaggregated prefill, highlighted by a newly opened UCCL P2P KV connector and hierarchical all-reduce with RDMA for multi-node tensor parallelism.

## Most important PRs
- **[#46269](https://github.com/vllm-project/vllm/pull/46269)** (Newly opened) Adds comprehensive support for the RWKV7 Albatross architecture, introducing necessary kernels and model definitions for the new RNN-based model.
- **[#43477](https://github.com/vllm-project/vllm/pull/43477)** (Merged) Enables DeepSeek V4 and GLM-5.1 on NVIDIA Blackwell (SM120) GPUs, wiring up FlashInfer, quantization, and speculative decoding paths for the new architecture.
- **[#43008](https://github.com/vllm-project/vllm/pull/43008)** (Merged) Introduces a cluster-cooperative topK kernel for DeepSeek V3.2 and V4, significantly reducing latency in MoE routing on NVIDIA hardware.
- **[#40835](https://github.com/vllm-project/vllm/pull/40835)** (Merged) Implements Triton-based INT4 per-token-head KV cache quantization, offering a major memory reduction for long-context inference while maintaining accuracy.
- **[#46583](https://github.com/vllm-project/vllm/pull/46583)** (Merged) Refactors the Rust frontend to use a unified parser interface and combined parser, streamlining tool calling and structured output generation.

## More changes by area

<details>
<summary>Performance (21)</summary>

- [#46546](https://github.com/vllm-project/vllm/pull/46546) (Merged) sparse attention optimization on minimax-m3
- [#46353](https://github.com/vllm-project/vllm/pull/46353) (Merged) Accelerate unquantized MoE for AArch64
- [#46202](https://github.com/vllm-project/vllm/pull/46202) (Merged) Enable chunked prefill and prefix caching for qwen3.5 on CPU
- [#46051](https://github.com/vllm-project/vllm/pull/46051) (Merged) Use dedicated runtime for HTTP/request-processing/ZMQ in Rust Frontend
- [#42235](https://github.com/vllm-project/vllm/pull/42235) (Merged) Add FlashInfer cutedsl NVFP4 GEMM backend
- [#45971](https://github.com/vllm-project/vllm/pull/45971) (Merged) Parallelize KV load with a receive-thread pool
- [#40784](https://github.com/vllm-project/vllm/pull/40784) (Merged) Tune wvSplitK on gfx1151
- [#46425](https://github.com/vllm-project/vllm/pull/46425) (Merged) reduce search space for thinking tokens
- [#43673](https://github.com/vllm-project/vllm/pull/43673) (Merged) DSv3.2: fuse MLA Q concat+fp8-quant in forward_mqa
- [#46392](https://github.com/vllm-project/vllm/pull/46392) (Merged) Enable + tune FlashInfer fused allreduce at world_size=16 on SM 10.3
- [#46542](https://github.com/vllm-project/vllm/pull/46542) (Merged) Replace O(n) list.index() with a dict in convert_mapping
- [#46543](https://github.com/vllm-project/vllm/pull/46543) (Merged) Avoid building a full timestamps list in video frame sampling
- [#46703](https://github.com/vllm-project/vllm/pull/46703) (Newly opened) Extend NCCL symmetric memory to AllGather and ReduceScatter
- [#46634](https://github.com/vllm-project/vllm/pull/46634) (Newly opened) Expand Triton kernel warmup coverage
- [#46545](https://github.com/vllm-project/vllm/pull/46545) (Newly opened) Shared-expert fusion for bias-routed MoE; enable on MiniMax-M3 mxfp8 model
- [#46474](https://github.com/vllm-project/vllm/pull/46474) (Newly opened) Fused shared expert for Minimax M3
- [#46275](https://github.com/vllm-project/vllm/pull/46275) (Newly opened) Enable split sparse decode on gfx942
- [#46635](https://github.com/vllm-project/vllm/pull/46635) (Newly opened) Replace MOE all-reduce with reduce-scatter
- [#46597](https://github.com/vllm-project/vllm/pull/46597) (Newly opened) Prefer ROCM_AITER_FA over ROCM_ATTN when AITER MHA is enabled
- [#46448](https://github.com/vllm-project/vllm/pull/46448) (Newly opened) Reduce TP communication for draft token generation
- [#46539](https://github.com/vllm-project/vllm/pull/46539) (Newly opened) Apply min-p in log-space to avoid a redundant softmax
- [#46540](https://github.com/vllm-project/vllm/pull/46540) (Newly opened) Reuse log-probs to avoid a second softmax in native sampler
- [#46323](https://github.com/vllm-project/vllm/pull/46323) (Newly opened) Erease the synconize h2d copy when enable samping params
</details>

<details>
<summary>Kernels & attention (34)</summary>

- [#45892](https://github.com/vllm-project/vllm/pull/45892) (Merged) BF16/FP8 Indexer using MSA for Minimax-M3
- [#45111](https://github.com/vllm-project/vllm/pull/45111) (Merged) Re-enable cross-layer KV cache layout for MLA via stride-aware kernels
- [#45181](https://github.com/vllm-project/vllm/pull/45181) (Merged) Support mixed KV page sizes for DFlash
- [#45703](https://github.com/vllm-project/vllm/pull/45703) (Merged) Extend Marlin thread-tile padding to MoE
- [#46167](https://github.com/vllm-project/vllm/pull/46167) (Merged) Add runtime monitor for post-warmup CuTeDSL compilation
- [#44044](https://github.com/vllm-project/vllm/pull/44044) (Merged) Support DCP with FP8 KV cache in MLA decode path
- [#46189](https://github.com/vllm-project/vllm/pull/46189) (Merged) Add FLASH_ATTN_MLA_SPARSE backend for Hopper sparse MLA
- [#44324](https://github.com/vllm-project/vllm/pull/44324) (Merged) Add RVV micro GEMM for WNA16
- [#44029](https://github.com/vllm-project/vllm/pull/44029) (Merged) Enable DFlash SD for CPU
- [#46385](https://github.com/vllm-project/vllm/pull/46385) (Merged) GLM5 Router GEMM
- [#45269](https://github.com/vllm-project/vllm/pull/45269) (Merged) Add RVV path for W4A8 INT4 GEMM
- [#45845](https://github.com/vllm-project/vllm/pull/45845) (Merged) Honor prefix-cache retention interval for Mamba/linear attention
- [#46393](https://github.com/vllm-project/vllm/pull/46393) (Merged) Add FlashInferCutedslMxfp8LinearKernel
- [#43081](https://github.com/vllm-project/vllm/pull/43081) (Merged) Support DFlash with FlashInfer
- [#36559](https://github.com/vllm-project/vllm/pull/36559) (Merged) Add swap AB optimization to fused_moe_kernel
- [#46522](https://github.com/vllm-project/vllm/pull/46522) (Newly opened) Prototype for Helion linear backend
- [#46699](https://github.com/vllm-project/vllm/pull/46699) (Newly opened) Add gfx950 HIP compressor path
- [#46326](https://github.com/vllm-project/vllm/pull/46326) (Newly opened) Add HiSparse MLA decode
- [#46514](https://github.com/vllm-project/vllm/pull/46514) (Newly opened) FlashMLA sparse: DCP on the fp8_ds_mla mixed-batch path + MTP
- [#46330](https://github.com/vllm-project/vllm/pull/46330) (Newly opened) FlashAttention prefill-context-parallel (PCP) support for GQA
- [#46676](https://github.com/vllm-project/vllm/pull/46676) (Newly opened) Native HIP MXFP4 for RDNA3
- [#46570](https://github.com/vllm-project/vllm/pull/46570) (Newly opened) Add MRV2 virtual-batch PCP for MLA
- [#46443](https://github.com/vllm-project/vllm/pull/46443) (Newly opened) DiffusionGemma: NVFP4 KV cache via FlashInfer VO-split + per-request causal grouping
- [#46329](https://github.com/vllm-project/vllm/pull/46329) (Newly opened) NVFP4 KV cache on consumer/SoC Blackwell for Gemma 3/4 via FlashInfer FA2
- [#46346](https://github.com/vllm-project/vllm/pull/46346) (Newly opened) Improve kkt kernel of CuteDSL prefill backend
- [#46485](https://github.com/vllm-project/vllm/pull/46485) (Newly opened) Add opt-in L20 paged decode path for FlashInfer
- [#46503](https://github.com/vllm-project/vllm/pull/46503) (Newly opened) Patch 4
- [#46682](https://github.com/vllm-project/vllm/pull/46682) (Newly opened) add helion nvfp4 backend for batch_size=1
- [#46718](https://github.com/vllm-project/vllm/pull/46718) (Newly opened) Add runtime monitor for post-warmup TileLang compilation
- [#46273](https://github.com/vllm-project/vllm/pull/46273) (Newly opened) Add fused SiLU+Mul+PerTokenQuant CUDA kernel
- [#46639](https://github.com/vllm-project/vllm/pull/46639) (Newly opened) Support batch invariance for WNA16 Marlin MoE
- [#46643](https://github.com/vllm-project/vllm/pull/46643) (Newly opened) Vectorized fp32 moe_sum reduction and support any topk
- [#46541](https://github.com/vllm-project/vllm/pull/46541) (Newly opened) Optimize FP8 group 128 quantization for Hopper
- [#46642](https://github.com/vllm-project/vllm/pull/46642) (Newly opened) Tune block-FP8 fused MoE for low-batch decode
- [#46340](https://github.com/vllm-project/vllm/pull/46340) (Newly opened) TD operand loads for batched MoE GEMM on XPU
- [#46638](https://github.com/vllm-project/vllm/pull/46638) (Newly opened) Add FlashInfer CuteDSL non-causal decode path for DFlash
- [#46713](https://github.com/vllm-project/vllm/pull/46713) (Newly opened) Batch Lookup in C
- [#46481](https://github.com/vllm-project/vllm/pull/46481) (Newly opened) NVFP4 grouped MoE: pingpong schedule at large per-exp
- [#46704](https://github.com/vllm-project/vllm/pull/46704) (Newly opened) Add sycl kernel mhc path for dsv4
</details>

<details>
<summary>MoE & quantization (19)</summary>

- [#46428](https://github.com/vllm-project/vllm/pull/46428) (Merged) Skip DP padding tokens in MoE
- [#43404](https://github.com/vllm-project/vllm/pull/43404) (Merged) add awq format for INCXPULinear
- [#46508](https://github.com/vllm-project/vllm/pull/46508) (Merged) Enable PDL for per_token_group_quant_8bit_kernel
- [#45375](https://github.com/vllm-project/vllm/pull/45375) (Merged) Enable modelopt_mixed on Turing
- [#46549](https://github.com/vllm-project/vllm/pull/46549) (Merged) Free unused MXFP4 scales in OAI Triton Backend
- [#46389](https://github.com/vllm-project/vllm/pull/46389) (Merged) Humming support for 2/3/5/6/7-bit pack-quantized weight-only inference
- [#44763](https://github.com/vllm-project/vllm/pull/44763) (Merged) Add weights padding for fp8 per-block online quantization
- [#45836](https://github.com/vllm-project/vllm/pull/45836) (Merged) Marlin: wire SwiGLU clamp + allow it for clamped models on non-Blackwell
- [#44517](https://github.com/vllm-project/vllm/pull/44517) (Merged) Pass gemm1_clamp_limit to XpuFusedMoe
- [#46528](https://github.com/vllm-project/vllm/pull/46528) (Newly opened) Enable asymmetric quant for Humming kernel
- [#46390](https://github.com/vllm-project/vllm/pull/46390) (Newly opened) enable humming wNaM inference for N=[23567] M=[48]
- [#46400](https://github.com/vllm-project/vllm/pull/46400) (Newly opened) Align online fp8_ptpc/block_fp8/mxfp8 weight quantization with llm-compressor
- [#46361](https://github.com/vllm-project/vllm/pull/46361) (Newly opened) Direct Register Custom Op for ARK
- [#46322](https://github.com/vllm-project/vllm/pull/46322) (Newly opened) Support hybrid INT4+FP8 AutoRound checkpoints
- [#46380](https://github.com/vllm-project/vllm/pull/46380) (Newly opened) Add MiniMax-M3 modelopt nvfp4 support
- [#46419](https://github.com/vllm-project/vllm/pull/46419) (Newly opened) Enable AITER MoE backend for MiniMax-M3-MXFP4
- [#46551](https://github.com/vllm-project/vllm/pull/46551) (Newly opened) Enable FlashInfer A2A for Minimax-M3-MXFP8
- [#46664](https://github.com/vllm-project/vllm/pull/46664) (Newly opened) Gate AITER MoE GateMode.INTERLEAVE on the gu-interleaved weight layout
- [#46629](https://github.com/vllm-project/vllm/pull/46629) (Newly opened) Add back emulation to available OCP MX backends list
</details>

<details>
<summary>Model support (13)</summary>

- [#45993](https://github.com/vllm-project/vllm/pull/45993) (Merged) Remove MiniMaxText01, MiniMaxVL01, MiniMaxForCausalLM
- [#44124](https://github.com/vllm-project/vllm/pull/44124) (Merged) support to OpenMOSS-Team
- [#46362](https://github.com/vllm-project/vllm/pull/46362) (Merged) Remove BaiChuanForCausalLM and BaichuanForCausalLM
- [#43132](https://github.com/vllm-project/vllm/pull/43132) (Merged) Add Qwen3 architecture support for EAGLE3
- [#46535](https://github.com/vllm-project/vllm/pull/46535) (Merged) Support EVS in Model Runner V2
- [#45555](https://github.com/vllm-project/vllm/pull/45555) (Merged) Add Qwen2-VL/Qwen2.5-VL processor-mapped video loader
- [#46623](https://github.com/vllm-project/vllm/pull/46623) (Newly opened) Add LongCat-Next multimodal model support
- [#46706](https://github.com/vllm-project/vllm/pull/46706) (Newly opened) Remove grok model arch from vllm
- [#46395](https://github.com/vllm-project/vllm/pull/46395) (Newly opened) Add locateanything model on support on XPU
- [#46564](https://github.com/vllm-project/vllm/pull/46564) (Newly opened) Support Unlimited OCR
- [#46286](https://github.com/vllm-project/vllm/pull/46286) (Newly opened) State-Aware Monolingual Constraints for DeepSeek-R1
- [#46609](https://github.com/vllm-project/vllm/pull/46609) (Newly opened) Add TorchCodec as a video decoding backend
- [#46646](https://github.com/vllm-project/vllm/pull/46646) (Newly opened) Enable all moe models for MRv2
</details>

<details>
<summary>Parallelism & scheduling (29)</summary>

- [#43468](https://github.com/vllm-project/vllm/pull/43468) (Merged) Self-describing KV events for OffloadingConnector
- [#45939](https://github.com/vllm-project/vllm/pull/45939) (Merged) add partial prefix cache primitives
- [#45053](https://github.com/vllm-project/vllm/pull/45053) (Merged) Replace OffloadingHandler with OffloadingWorker
- [#46039](https://github.com/vllm-project/vllm/pull/46039) (Merged) Support MiniMax-M3 mixed KV layouts in MoRIIO READ mode
- [#46332](https://github.com/vllm-project/vllm/pull/46332) (Merged) Support MoRIIO heterogeneous TP fan-in
- [#46412](https://github.com/vllm-project/vllm/pull/46412) (Merged) Only check and store new KV cache range in Mooncake
- [#45957](https://github.com/vllm-project/vllm/pull/45957) (Merged) Add labeled metrics support for KV Offloading
- [#46363](https://github.com/vllm-project/vllm/pull/46363) (Merged) Replace bool|None lookup return with LookupResult enum
- [#45013](https://github.com/vllm-project/vllm/pull/45013) (Merged) Enable nixl eplb communicator for elastic ep
- [#45959](https://github.com/vllm-project/vllm/pull/45959) (Merged) Add tiering metric plumbing
- [#45810](https://github.com/vllm-project/vllm/pull/45810) (Merged) Add pipeline parallelism support for MiniMax-M3
- [#45850](https://github.com/vllm-project/vllm/pull/45850) (Merged) Use background thread for mmap / cpu_tensors pinning
- [#45080](https://github.com/vllm-project/vllm/pull/45080) (Merged) DecodeBenchConnector: fill list/tuple KV caches
- [#46188](https://github.com/vllm-project/vllm/pull/46188) (Merged) Optimize lookup pool key string construction
- [#46216](https://github.com/vllm-project/vllm/pull/46216) (Merged) Maintain evictable list in LRUCachePolicy
- [#46432](https://github.com/vllm-project/vllm/pull/46432) (Merged) Fill invalid recv_topk_idx with -1
- [#46532](https://github.com/vllm-project/vllm/pull/46532) (Merged) Throttle prefills based on local prefill work
- [#46404](https://github.com/vllm-project/vllm/pull/46404) (Merged) Bound num_max_tokens_per_rank in do_expand=False
- [#46473](https://github.com/vllm-project/vllm/pull/46473) (Merged) Disable bidirectional xfer mode for NixlPushConnector
- [#46498](https://github.com/vllm-project/vllm/pull/46498) (Newly opened) Add UcclP2pConnector for disaggregated prefill over UCCL P2P
- [#46370](https://github.com/vllm-project/vllm/pull/46370) (Newly opened) Initial support for fault tolerant ep using scale-down
- [#46387](https://github.com/vllm-project/vllm/pull/46387) (Newly opened) Multi-view NIXL connector
- [#46447](https://github.com/vllm-project/vllm/pull/46447) (Newly opened) Add hierarchical all-reduce with RDMA for multi-node tensor parallelism
- [#46384](https://github.com/vllm-project/vllm/pull/46384) (Newly opened) support partial prefix cache hits in hybrid coordinator
- [#46504](https://github.com/vllm-project/vllm/pull/46504) (Newly opened) Infer control interface and clarify network setup
- [#46556](https://github.com/vllm-project/vllm/pull/46556) (Newly opened) Per-worker disk tier + LRU write-back for symmetric multi-node KV cache
- [#46483](https://github.com/vllm-project/vllm/pull/46483) (Newly opened) Mistral Large 3 EPLB Support
- [#46544](https://github.com/vllm-project/vllm/pull/46544) (Newly opened) Emit secondary-tier BlockStored presence events
- [#46397](https://github.com/vllm-project/vllm/pull/46397) (Newly opened) Add KV Events to SimpleCPUOffloadConnector
</details>

<details>
<summary>Hardware & arch (5)</summary>

- [#46135](https://github.com/vllm-project/vllm/pull/46135) (Merged) Enable fp16 support for PowerPC
- [#46141](https://github.com/vllm-project/vllm/pull/46141) (Merged) Query total device memory via amdsmi to avoid HIP init
- [#46636](https://github.com/vllm-project/vllm/pull/46636) (Merged) Begin Deprecation Window for CUDA_VISIBLE_DEVICES on ROCm
- [#46516](https://github.com/vllm-project/vllm/pull/46516) (Newly opened) Enable gfx1250 ROCm architecture
- [#46606](https://github.com/vllm-project/vllm/pull/46606) (Newly opened) Support Vit CudaGraph for v2
</details>

<details>
<summary>API & serving (30)</summary>

- [#44285](https://github.com/vllm-project/vllm/pull/44285) (Merged) Split ServingRender into renderer and entrypoint
- [#46584](https://github.com/vllm-project/vllm/pull/46584) (Merged) Make ToolParserOutput a seq of ToolParserEvent
- [#46314](https://github.com/vllm-project/vllm/pull/46314) (Merged) Port seed_oss to streaming parser engine
- [#46057](https://github.com/vllm-project/vllm/pull/46057) (Merged) Integrate xgrammar-structural-tag for strict/required tool calling
- [#46219](https://github.com/vllm-project/vllm/pull/46219) (Merged) Support echo for token-ID completion prompts
- [#46359](https://github.com/vllm-project/vllm/pull/46359) (Merged) Correct --reasoning-parser semantics
- [#46360](https://github.com/vllm-project/vllm/pull/46360) (Merged) Pass effective reasoning_parser_kwargs for structured output
- [#46137](https://github.com/vllm-project/vllm/pull/46137) (Merged) Support thinking_token_budget for chat and completions
- [#46348](https://github.com/vllm-project/vllm/pull/46348) (Merged) Align Rust allowed_token_ids validation with Python
- [#46457](https://github.com/vllm-project/vllm/pull/46457) (Merged) Filter Pydantic-internal markers from validation error param
- [#46096](https://github.com/vllm-project/vllm/pull/46096) (Merged) Generalize use of WhisperModelState
- [#46582](https://github.com/vllm-project/vllm/pull/46582) (Merged) Raise frontend JSON body limit
- [#44610](https://github.com/vllm-project/vllm/pull/44610) (Merged) Forward VLLM_ENGINE_READY_TIMEOUT_S via --args-json
- [#44638](https://github.com/vllm-project/vllm/pull/44638) (Merged) return routed_experts on streaming generate responses
- [#46602](https://github.com/vllm-project/vllm/pull/46602) (Newly opened) Migrate gemma4 to unified parser
- [#46350](https://github.com/vllm-project/vllm/pull/46350) (Newly opened) Add TLS support with certificate/key files
- [#46427](https://github.com/vllm-project/vllm/pull/46427) (Newly opened) Add generative scoring route
- [#46610](https://github.com/vllm-project/vllm/pull/46610) (Newly opened) Add Streaming Parser Engine and new Kimi k2.5/k2.6/k2.7 Parser
- [#46369](https://github.com/vllm-project/vllm/pull/46369) (Newly opened) Add step3 tool parser
- [#46306](https://github.com/vllm-project/vllm/pull/46306) (Newly opened) expose profiler control routes in Rust frontend
- [#46617](https://github.com/vllm-project/vllm/pull/46617) (Newly opened) Add Jamba tool parser
- [#46507](https://github.com/vllm-project/vllm/pull/46507) (Newly opened) Make Granite4 string argument scanning incremental
- [#46547](https://github.com/vllm-project/vllm/pull/46547) (Newly opened) Plumb request session id to Mooncake worker
- [#46709](https://github.com/vllm-project/vllm/pull/46709) (Newly opened) Add longcat tool parser support
- [#46437](https://github.com/vllm-project/vllm/pull/46437) (Newly opened) Use process_eos() to flush Harmony Parser outputs
- [#46415](https://github.com/vllm-project/vllm/pull/46415) (Newly opened) Sanitize server file paths from validation error responses
- [#46279](https://github.com/vllm-project/vllm/pull/46279) (Newly opened) Support --max-log-len
- [#46680](https://github.com/vllm-project/vllm/pull/46680) (Newly opened) Support srt response format for audio transcription
- [#46684](https://github.com/vllm-project/vllm/pull/46684) (Newly opened) add repetition_detection support to sampling params across Rust frontend
- [#46331](https://github.com/vllm-project/vllm/pull/46331) (Newly opened) Add non-blocking get_output_nowait() to engine core client
- [#46512](https://github.com/vllm-project/vllm/pull/46512) (Newly opened) Add error context in tool parser failures
- [#46438](https://github.com/vllm-project/vllm/pull/46438) (Newly opened) Add CuMemAllocator.discard() for tag-selective GPU memory release
- [#46677](https://github.com/vllm-project/vllm/pull/46677) (Newly opened) Accept chat-completions image format on /v1/responses
</details>

<details>
<summary>Tests (31)</summary>

- [#45424](https://github.com/vllm-project/vllm/pull/45424) (Merged) Ensure memory is pinned prior to async h2d copy
- [#46355](https://github.com/vllm-project/vllm/pull/46355) (Merged) Add unit tests for OffloadingSpecFactory and SecondaryTierFactory
- [#45931](https://github.com/vllm-project/vllm/pull/45931) (Merged) Disable TileLang MHC dispatch on gfx942
- [#46533](https://github.com/vllm-project/vllm/pull/46533) (Merged) Reject placeholder draft tokens in rejection sampler
- [#46252](https://github.com/vllm-project/vllm/pull/46252) (Merged) Gate packed HMA KV cache on cross-layer config
- [#46431](https://github.com/vllm-project/vllm/pull/46431) (Merged) Skip Quark mxfp4 tests unless Quark version is compatible
- [#46160](https://github.com/vllm-project/vllm/pull/46160) (Merged) Skip unsupported test cases on ROCm
- [#46494](https://github.com/vllm-project/vllm/pull/46494) (Merged) Remove BaiChuanForCausalLM from the LoRA test
- [#46401](https://github.com/vllm-project/vllm/pull/46401) (Merged) Restrict MLA cross-layer KV cache test to supported backends on ROCm
- [#45914](https://github.com/vllm-project/vllm/pull/45914) (Merged) Pin block_size in auto-fit max_model_len test
- [#46161](https://github.com/vllm-project/vllm/pull/46161) (Merged) Add TP=4 requirement to test_mixed_precision_model_accuracies
- [#46241](https://github.com/vllm-project/vllm/pull/46241) (Merged) Replace InternVL2-1B with InternVL3-1B in test_pipeline_parallel.py
- [#45772](https://github.com/vllm-project/vllm/pull/45772) (Merged) Torch 2.11 flaky test_spec_decode_logprobs and gritlm tests
- [#46580](https://github.com/vllm-project/vllm/pull/46580) (Merged) Skip the MoE Marlin tile-padding helper assertion
- [#46352](https://github.com/vllm-project/vllm/pull/46352) (Merged) Temporarily skip M3 on CI
- [#46592](https://github.com/vllm-project/vllm/pull/46592) (Newly opened) Feat/invariant with prefix cache
- [#46475](https://github.com/vllm-project/vllm/pull/46475) (Newly opened) Add unit tests for five untested utility modules
- [#46416](https://github.com/vllm-project/vllm/pull/46416) (Newly opened) Add streaming invariant tests
- [#46478](https://github.com/vllm-project/vllm/pull/46478) (Newly opened) honour skip_kv_gather in AITER MLA sparse prefill chunk loop
- [#46499](https://github.com/vllm-project/vllm/pull/46499) (Newly opened) Add Gumbel sampler benchmark for speculative decoding
- [#46274](https://github.com/vllm-project/vllm/pull/46274) (Newly opened) Add Qwen3 streaming tool-call regression tests
- [#46538](https://github.com/vllm-project/vllm/pull/46538) (Newly opened) Skip building unused per-step scheduler-output fields
- [#46289](https://github.com/vllm-project/vllm/pull/46289) (Newly opened) Reclaim KV blocks leaked by aborted remote KV recv
- [#46337](https://github.com/vllm-project/vllm/pull/46337) (Newly opened) Migrate weight-offloading env vars to OffloadConfig
- [#46450](https://github.com/vllm-project/vllm/pull/46450) (Newly opened) Pass ScheduleEndContext to on_schedule_end hook
- [#46523](https://github.com/vllm-project/vllm/pull/46523) (Newly opened) Prewarm full cudagraph capture forward pass
- [#46349](https://github.com/vllm-project/vllm/pull/46349) (Newly opened) run MoRIIO layout geometry on CPU
- [#46491](https://github.com/vllm-project/vllm/pull/46491) (Newly opened) Revert Mxfp4MoeBackend.TRITON_UNFUSED fallback
- [#46434](https://github.com/vllm-project/vllm/pull/46434) (Newly opened) Enable modular OAI Triton MoE tests
- [#46658](https://github.com/vllm-project/vllm/pull/46658) (Newly opened) Relax fused layernorm quant test tolerances for one-ULP outliers
- [#46468](https://github.com/vllm-project/vllm/pull/46468) (Newly opened) xfail fused TRITON MXFP4 MoE accuracy on gfx950
- [#46267](https://github.com/vllm-project/vllm/pull/46267) (Newly opened) Resurrect test_rocm_mxfp4_moe_oracle
</details>

<details>
<summary>CI & build (33)</summary>

- [#46418](https://github.com/vllm-project/vllm/pull/46418) (Merged) Purging away redundant test group definitions
- [#46573](https://github.com/vllm-project/vllm/pull/46573) (Merged) Expand basic correctness target suites
- [#45768](https://github.com/vllm-project/vllm/pull/45768) (Merged) Add agent_tags for Intel GPU CI
- [#46537](https://github.com/vllm-project/vllm/pull/46537) (Merged) Stage C-II of gating additional test groups
- [#43752](https://github.com/vllm-project/vllm/pull/43752) (Merged) add humming lm-eval test
- [#45869](https://github.com/vllm-project/vllm/pull/45869) (Merged) pass merge-base to container for python-only wheel metadata
- [#45973](https://github.com/vllm-project/vllm/pull/45973) (Merged) switch to ubuntu 24.04 as base image
- [#39541](https://github.com/vllm-project/vllm/pull/39541) (Merged) Add DGX Spark GPQA smoke test
- [#46327](https://github.com/vllm-project/vllm/pull/46327) (Merged) update nixl to v1.2.0
- [#45955](https://github.com/vllm-project/vllm/pull/45955) (Merged) Enable kv_connector unit tests on ROCm
- [#45967](https://github.com/vllm-project/vllm/pull/45967) (Merged) skip test_double_aiter_rms_quant_fusion
- [#46520](https://github.com/vllm-project/vllm/pull/46520) (Merged) Shard LM Eval Qwen3-5 Models in AMD CI
- [#46386](https://github.com/vllm-project/vllm/pull/46386) (Merged) Run DeepSeek-V2-Lite prefetch-offload eval eager on ROCm
- [#46517](https://github.com/vllm-project/vllm/pull/46517) (Merged) Remove redundant flashinfer download-cubin step
- [#46686](https://github.com/vllm-project/vllm/pull/46686) (Merged) Move Metrics, Tracing & make optional
- [#46674](https://github.com/vllm-project/vllm/pull/46674) (Merged) Refine .buildkite/ci_config_intel.yaml for Intel GPU CI
- [#46702](https://github.com/vllm-project/vllm/pull/46702) (Merged) Allow more CPU CI agents
- [#46590](https://github.com/vllm-project/vllm/pull/46590) (Newly opened) add intel full ci job yamls
- [#46653](https://github.com/vllm-project/vllm/pull/46653) (Newly opened) DO NOT MERGE
- [#46374](https://github.com/vllm-project/vllm/pull/46374) (Newly opened) add xpu release pipeline
- [#46696](https://github.com/vllm-project/vllm/pull/46696) (Newly opened) Switch rustls to native-tls/OpenSSL
- [#46403](https://github.com/vllm-project/vllm/pull/46403) (Newly opened) Bump the minor-update group across 1 directory
- [#46527](https://github.com/vllm-project/vllm/pull/46527) (Newly opened) Cache Rust builds by source inputs
- [#46496](https://github.com/vllm-project/vllm/pull/46496) (Newly opened) 阿
- [#46510](https://github.com/vllm-project/vllm/pull/46510) (Newly opened) Update requirements to use PyTorch nightly wheels
- [#46660](https://github.com/vllm-project/vllm/pull/46660) (Newly opened) Build macOS arm64 CPU wheels via GitHub-hosted runners
- [#46433](https://github.com/vllm-project/vllm/pull/46433) (Newly opened) Constrain subprocess ZE_AFFINITY_MASK to local_world_size
- [#46599](https://github.com/vllm-project/vllm/pull/46599) (Newly opened) Rename build stages for clarity
- [#46711](https://github.com/vllm-project/vllm/pull/46711) (Newly opened) Add registry layer cache to x86 CUDA release image builds
- [#46705](https://github.com/vllm-project/vllm/pull/46705) (Newly opened) Migrate Voxtral to mistral-common 1.11.4 audio API
- [#46456](https://github.com/vllm-project/vllm/pull/46456) (Newly opened) intel CI: add quantization and awq case for xpu
- [#46487](https://github.com/vllm-project/vllm/pull/46487) (Newly opened) Support lora serialize and deserialize
- [#46668](https://github.com/vllm-project/vllm/pull/46668) (Newly opened) Mirror Basic Models and Weight Loading Multiple GPU test groups
- [#46691](https://github.com/vllm-project/vllm/pull/46691) (Newly opened) Use Triton-based AITER MHA for LM Eval Qwen-3.5 Models Tests
- [#46683](https://github.com/vllm-project/vllm/pull/46683) (Newly opened) Bump flashinfer version to 0.6.13
</details>

<details>
<summary>Docs (11)</summary>

- [#46197](https://github.com/vllm-project/vllm/pull/46197) (Merged) Add Qwen3 forced alignment online example
- [#46398](https://github.com/vllm-project/vllm/pull/46398) (Merged) Fix typos, grammar, and broken commands across docs
- [#46376](https://github.com/vllm-project/vllm/pull/46376) (Merged) Document pull request limit
- [#46605](https://github.com/vllm-project/vllm/pull/46605) (Merged) Remove AquilaForCausalLM, AquilaModel
- [#40469](https://github.com/vllm-project/vllm/pull/40469) (Merged) Fix minor doc sentence, grammar, quote errors
- [#46373](https://github.com/vllm-project/vllm/pull/46373) (Merged) link security docs from AGENTS
- [#45940](https://github.com/vllm-project/vllm/pull/45940) (Merged) Update MiniMax-M3
- [#44720](https://github.com/vllm-project/vllm/pull/44720) (Merged) Document Qwen3.6 ViT CUDA graph support
- [#46687](https://github.com/vllm-project/vllm/pull/46687) (Newly opened) document NIXL KV connector transfer metrics aggregation logic
- [#46701](https://github.com/vllm-project/vllm/pull/46701) (Newly opened) Support trace_decode_token_ids for deterministic decode replay
- [#46336](https://github.com/vllm-project/vllm/pull/46336) (Newly opened) Add execution trace capture to torch profiler config
</details>

<details>
<summary>Bugfixes (107)</summary>

- [#46290](https://github.com/vllm-project/vllm/pull/46290) (Merged) Fix MoRIIO WRITE mode for mixed KV layouts
- [#46344](https://github.com/vllm-project/vllm/pull/46344) (Merged) Fix Kimi K2 tool call IDs for required tool choice
- [#46284](https://github.com/vllm-project/vllm/pull/46284) (Merged) Fix KV offload request-finished lifecycle contract
- [#39896](https://github.com/vllm-project/vllm/pull/39896) (Merged) Fix mypy for vllm/benchmarks
- [#45718](https://github.com/vllm-project/vllm/pull/45718) (Merged) Parse MiniMax M3 streaming reasoning by text markers
- [#46315](https://github.com/vllm-project/vllm/pull/46315) (Merged) Fix EAGLE drafter multimodal encoder cache misses
- [#46278](https://github.com/vllm-project/vllm/pull/46278) (Merged) Fix SimpleCPUOffloadConnector GPU->CPU store race
- [#46406](https://github.com/vllm-project/vllm/pull/46406) (Merged) Support non-power-of-2 top_k in legacy triton_kernels routing
- [#45935](https://github.com/vllm-project/vllm/pull/45935) (Merged) Fix MiniMaxM2ForCausalLM perf regression
- [#45219](https://github.com/vllm-project/vllm/pull/45219) (Merged) Fix nixl tests
- [#41722](https://github.com/vllm-project/vllm/pull/41722) (Merged) Fix mypy for vllm/lora
- [#46351](https://github.com/vllm-project/vllm/pull/46351) (Merged) fix: stream Qwen3 tool call string arguments
- [#45048](https://github.com/vllm-project/vllm/pull/45048) (Merged) GPT-OSS Autodrop reasoning in Response API and cleanup
- [#44053](https://github.com/vllm-project/vllm/pull/44053) (Merged) Reserve workspace before CUDA graph capture
- [#46203](https://github.com/vllm-project/vllm/pull/46203) (Merged) Fix cumem sleep and teardown
- [#44105](https://github.com/vllm-project/vllm/pull/44105) (Merged) Omit empty tool_calls from OpenAI chat responses
- [#45389](https://github.com/vllm-project/vllm/pull/45389) (Merged) Handle braces in required tool streaming strings
- [#46231](https://github.com/vllm-project/vllm/pull/46231) (Merged) Defer offload reads while transfers are pending
- [#44361](https://github.com/vllm-project/vllm/pull/44361) (Merged) Responses API assistant EasyInputMessageParam input
- [#46560](https://github.com/vllm-project/vllm/pull/46560) (Merged) Fix int32 offset overflow in sampler kernels
- [#46080](https://github.com/vllm-project/vllm/pull/46080) (Merged) Fix Kernels Attention test groups
- [#41161](https://github.com/vllm-project/vllm/pull/41161) (Merged) Fix static actorder handling for compressed-tensors WNA16 MoE
- [#46394](https://github.com/vllm-project/vllm/pull/46394) (Merged) Fix remaining global→block conversions under PCP/DCP
- [#46408](https://github.com/vllm-project/vllm/pull/46408) (Merged) Support -1 slots in topk_ids for Triton MoE
- [#46114](https://github.com/vllm-project/vllm/pull/46114) (Merged) Fix chunk alignment when using context parallelism with TRITON_MLA
- [#46142](https://github.com/vllm-project/vllm/pull/46142) (Merged) Fix tests to not dispatch on UNFUSED_TRITON backend on MI300
- [#46414](https://github.com/vllm-project/vllm/pull/46414) (Merged) Fix AITER FP8 quantization schema tests
- [#46595](https://github.com/vllm-project/vllm/pull/46595) (Merged) track resumed requests via scheduler's resumed_req_ids
- [#46108](https://github.com/vllm-project/vllm/pull/46108) (Merged) ColQwen3.5: fix retrieval correctness
- [#46308](https://github.com/vllm-project/vllm/pull/46308) (Merged) Emit non-ASCII tool-call arguments without escapes
- [#45361](https://github.com/vllm-project/vllm/pull/45361) (Merged) Fix INT8 per-token-head KV cache rounding in Triton reshape-and-cache
- [#46305](https://github.com/vllm-project/vllm/pull/46305) (Merged) Fix multi-video crash with list-valued fps/num_frames
- [#44434](https://github.com/vllm-project/vllm/pull/44434) (Merged) enable shared expert fusion for Qwen3.5
- [#45100](https://github.com/vllm-project/vllm/pull/45100) (Merged) Avoid racy accepted counts in async spec decode
- [#46379](https://github.com/vllm-project/vllm/pull/46379) (Merged) Fix swap_blocks_batch on the default stream
- [#46463](https://github.com/vllm-project/vllm/pull/46463) (Merged) prevent infinite loop in split_audio with NaN audio
- [#46525](https://github.com/vllm-project/vllm/pull/46525) (Merged) Emit a content block for empty Anthropic completions
- [#46298](https://github.com/vllm-project/vllm/pull/46298) (Merged) Fix gfx942 Kernels MoE test group
- [#43362](https://github.com/vllm-project/vllm/pull/43362) (Merged) FusedMoE: coerce shape-(1,) per-tensor scales to 0-D scalar
- [#46382](https://github.com/vllm-project/vllm/pull/46382) (Merged) fix: stream Mimimax m2 tool call string arguments
- [#46420](https://github.com/vllm-project/vllm/pull/46420) (Merged) Fix humming lm_head crash and FusedMoE weight_shape coercion
- [#46260](https://github.com/vllm-project/vllm/pull/46260) (Merged) Fix stale test_gfx950_moe MXFP4 oracle tests
- [#46313](https://github.com/vllm-project/vllm/pull/46313) (Merged) Reject matryoshka embedding dimensions above hidden size
- [#46254](https://github.com/vllm-project/vllm/pull/46254) (Merged) Fix NVFP4/OCP MX MoE emulation
- [#46018](https://github.com/vllm-project/vllm/pull/46018) (Merged) Fix Spec Decode Eagle test group
- [#46495](https://github.com/vllm-project/vllm/pull/46495) (Merged) Fix NemotronLayerNorm1P hardcoded cuda device type
- [#45956](https://github.com/vllm-project/vllm/pull/45956) (Merged) Fix probabilistic sampling for parallel drafting
- [#46550](https://github.com/vllm-project/vllm/pull/46550) (Merged) Fix topk histogram build on SM75
- [#44483](https://github.com/vllm-project/vllm/pull/44483) (Merged) Fix illegal memory access from a forward during a partial wake_up
- [#46548](https://github.com/vllm-project/vllm/pull/46548) (Merged) Fix OOB During Model Warmup With ROCM_ATTN and MRV2
- [#46650](https://github.com/vllm-project/vllm/pull/46650) (Merged) Fix Pipeline + Context Parallelism test group
- [#46245](https://github.com/vllm-project/vllm/pull/46245) (Merged) Preserve all allowed_token_ids in the logit bias kernel
- [#46467](https://github.com/vllm-project/vllm/pull/46467) (Merged) Fix duplicated logging when loading a corrupt or partial video
- [#46435](https://github.com/vllm-project/vllm/pull/46435) (Merged) Fix lm head sharing for dflash
- [#45715](https://github.com/vllm-project/vllm/pull/45715) (Merged) Gate all_gather on fully_sharded_loras inside _mcp_apply
- [#46220](https://github.com/vllm-project/vllm/pull/46220) (Merged) Keep pydantic validation for fields with a TYPE_CHECKING Literal alias
- [#46113](https://github.com/vllm-project/vllm/pull/46113) (Merged) Fix stop string truncation with repeated matches
- [#46627](https://github.com/vllm-project/vllm/pull/46627) (Merged) Fix IndentationError: expected an indented block after 'with' statement
- [#46341](https://github.com/vllm-project/vllm/pull/46341) (Merged) Fix Llama4ForCausalLM initialization test failure
- [#46101](https://github.com/vllm-project/vllm/pull/46101) (Merged) Normalize slashes in Helion GPU names
- [#46163](https://github.com/vllm-project/vllm/pull/46163) (Merged) Fix missing tp_size attribute on RoutedExperts
- [#45404](https://github.com/vllm-project/vllm/pull/45404) (Merged) access tp_size via moe_config for RoutedExperts compatibility
- [#46410](https://github.com/vllm-project/vllm/pull/46410) (Merged) fix fp8 range in vit_fp8_quant
- [#45818](https://github.com/vllm-project/vllm/pull/45818) (Merged) Fix unquantized gpt-oss weight loading broken by FusedMoE
- [#46339](https://github.com/vllm-project/vllm/pull/46339) (Merged) Re-enable FP8 MoE on NVIDIA Thor
- [#44665](https://github.com/vllm-project/vllm/pull/44665) (Merged) Fix memory pointer overflow in Mamba state buffers
- [#46365](https://github.com/vllm-project/vllm/pull/46365) (Merged) Fix CPU model runner v2
- [#46069](https://github.com/vllm-project/vllm/pull/46069) (Merged) Accept USE_FP64_GUMBEL in CPU recovered-tokens sampler
- [#46164](https://github.com/vllm-project/vllm/pull/46164) (Merged) Fix test_auto_gptq on ROCm CI
- [#46243](https://github.com/vllm-project/vllm/pull/46243) (Merged) Fix min_tokens off-by-one in the V2 GPU sampler
- [#46529](https://github.com/vllm-project/vllm/pull/46529) (Newly opened) Thread token IDs through non-streaming paths of parser engine
- [#46285](https://github.com/vllm-project/vllm/pull/46285) (Newly opened) Handle missing req_id in update_from_output() with PP + tool-calling
- [#46558](https://github.com/vllm-project/vllm/pull/46558) (Newly opened) Enable FlashInfer mm-prefix attention
- [#46271](https://github.com/vllm-project/vllm/pull/46271) (Newly opened) Fix for issue #15697
- [#46455](https://github.com/vllm-project/vllm/pull/46455) (Newly opened) Hybrid Mamba + KV connector: reconcile diverged per-group prefix hits
- [#46652](https://github.com/vllm-project/vllm/pull/46652) (Newly opened) Calculate ITL using exact token delta from usage stats
- [#46486](https://github.com/vllm-project/vllm/pull/46486) (Newly opened) PoolsideV1: fix string whitespace and required named tool choice
- [#46700](https://github.com/vllm-project/vllm/pull/46700) (Newly opened) Cap repetition_detection window to bound scheduler CPU
- [#46301](https://github.com/vllm-project/vllm/pull/46301) (Newly opened) Fix hidden-state extraction block size for hybrid verifiers
- [#46477](https://github.com/vllm-project/vllm/pull/46477) (Newly opened) cap mem_get_info total to local VRAM to fix 192 GiB over-allocation
- [#46471](https://github.com/vllm-project/vllm/pull/46471) (Newly opened) Gracefully handle Harmony parser errors
- [#46334](https://github.com/vllm-project/vllm/pull/46334) (Newly opened) Mooncake: honor logical->physical block ratio in register_kv_caches
- [#46446](https://github.com/vllm-project/vllm/pull/46446) (Newly opened) Warm up slot-mapping kernel through BlockTable
- [#46454](https://github.com/vllm-project/vllm/pull/46454) (Newly opened) Fix DiffusionGemma GGUF tied embedding loading
- [#46645](https://github.com/vllm-project/vllm/pull/46645) (Newly opened) Fix gpt-oss-20b NVFP4 inference
- [#46666](https://github.com/vllm-project/vllm/pull/46666) (Newly opened) Exclude disagg P/D transfer tokens from cached_tokens
- [#46695](https://github.com/vllm-project/vllm/pull/46695) (Newly opened) Fix FlashAttnMLA FP8 KV cache support
- [#46714](https://github.com/vllm-project/vllm/pull/46714) (Newly opened) fix misleading docstrings in non-impacting config compute_hash
- [#46521](https://github.com/vllm-project/vllm/pull/46521) (Newly opened) Treat QUTLASS extension as optional
- [#46574](https://github.com/vllm-project/vllm/pull/46574) (Newly opened) sanitize invalid speculative draft tokens
- [#46257](https://github.com/vllm-project/vllm/pull/46257) (Newly opened) DeepSeek-V4 tokenizer: honor add_generation_prompt
- [#46304](https://github.com/vllm-project/vllm/pull/46304) (Newly opened) Skip stale KV xfer finish notifications for already-freed requests
- [#46690](https://github.com/vllm-project/vllm/pull/46690) (Newly opened) Fix UVA offload fallback copies
- [#46281](https://github.com/vllm-project/vllm/pull/46281) (Newly opened) Align hybrid model prefix cache hit lengths to prevent block missing on EAGLE
- [#46476](https://github.com/vllm-project/vllm/pull/46476) (Newly opened) Fix KeyError in PP2 when last stage finishes request via tool-call parser
- [#46601](https://github.com/vllm-project/vllm/pull/46601) (Newly opened) Fix Marlin repack PTX incompatibility on H100/H200
- [#46276](https://github.com/vllm-project/vllm/pull/46276) (Newly opened) weights processing peak memory reduction for nvfp4 MoE layers
- [#46287](https://github.com/vllm-project/vllm/pull/46287) (Newly opened) contain filesystem resolver paths
- [#46371](https://github.com/vllm-project/vllm/pull/46371) (Newly opened) guard init_fp8_kv_scales against unallocated tensors during wake up
- [#46319](https://github.com/vllm-project/vllm/pull/46319) (Newly opened) fix: resolve issue #22225
- [#46469](https://github.com/vllm-project/vllm/pull/46469) (Newly opened) Add regression test for vision encoder MATH SDPA backend
- [#46399](https://github.com/vllm-project/vllm/pull/46399) (Newly opened) Disable dynamic speculative decoding for fixed-K proposers instead of crashing
- [#46515](https://github.com/vllm-project/vllm/pull/46515) (Newly opened) Fix IPC handle leak in CustomAllreduce during CUDA graph memory profiling
- [#46292](https://github.com/vllm-project/vllm/pull/46292) (Newly opened) fix: resolve issue #42426
- [#46451](https://github.com/vllm-project/vllm/pull/46451) (Newly opened) Fix multimodal cache desync after input rejection
- [#46663](https://github.com/vllm-project/vllm/pull/46663) (Newly opened) Fix reasoning-end detection to check prompt tail only
- [#46294](https://github.com/vllm-project/vllm/pull/46294) (Newly opened) fix: resolve issue #22519
- [#46280](https://github.com/vllm-project/vllm/pull/46280) (Newly opened) YaRN RoPE: honor explicit attention_factor from the rope config
- [#46342](https://github.com/vllm-project/vllm/pull/46342) (Newly opened) fix: resolve issue #37729
- [#46554](https://github.com/vllm-project/vllm/pull/46554) (Newly opened) Lazy-grow InputBatch token_ids_cpu / is_token_ids buffers
- [#46377](https://github.com/vllm-project/vllm/pull/46377) (Newly opened) Resample long audio in blocks to avoid int32 AudioFrame overflow
- [#46489](https://github.com/vllm-project/vllm/pull/46489) (Newly opened) Avoid embedding padded runner token ids
- [#46689](https://github.com/vllm-project/vllm/pull/46689) (Newly opened) Skip PP sampled-token broadcast on KV producer
- [#46697](https://github.com/vllm-project/vllm/pull/46697) (Newly opened) Add CPU fallback for mamba batch memcpy
- [#46409](https://github.com/vllm-project/vllm/pull/46409) (Newly opened) Fix test_concat_and_cache_mla_rope_fused on ROCm
- [#46567](https://github.com/vllm-project/vllm/pull/46567) (Newly opened) Fix model info cache for package models
- [#46375](https://github.com/vllm-project/vllm/pull/46375) (Newly opened) resolve memory allocation and buffer overflow in audio resampling
- [#46612](https://github.com/vllm-project/vllm/pull/46612) (Newly opened) Raise VLLMValidationError for non-integer logit_bias keys
- [#46616](https://github.com/vllm-project/vllm/pull/46616) (Newly opened) Balance MiniMax M3 reasoning markers in is_reasoning_end
- [#46694](https://github.com/vllm-project/vllm/pull/46694) (Newly opened) Fix NIXL async KV load lookahead handling for MTP spec decode
- [#46662](https://github.com/vllm-project/vllm/pull/46662) (Newly opened) Rd fix spec tb combine overhead
- [#46259](https://github.com/vllm-project/vllm/pull/46259) (Newly opened) Revert "[Hardware][AMD][CI] Fix e2e core test group"
- [#46614](https://github.com/vllm-project/vllm/pull/46614) (Newly opened) Parse compact sentence-transformers pooling_mode
- [#46708](https://github.com/vllm-project/vllm/pull/46708) (Newly opened) Fix make_valid_python backslash-escape edge case
- [#46461](https://github.com/vllm-project/vllm/pull/46461) (Newly opened) Add continuation guard to fast-path to prevent prefix K/V loss
- [#46681](https://github.com/vllm-project/vllm/pull/46681) (Newly opened) Disable packed KV cache allocation on XPU for DeepSeek-V4
- [#46552](https://github.com/vllm-project/vllm/pull/46552) (Newly opened) Transformers backend: recompute mm_token_type_ids per request for M-RoPE
- [#46561](https://github.com/vllm-project/vllm/pull/46561) (Newly opened) Actionable error for desc_act GPTQ models requiring fp16
- [#46296](https://github.com/vllm-project/vllm/pull/46296) (Newly opened) fix: resolve issue #17676
- [#46310](https://github.com/vllm-project/vllm/pull/46310) (Newly opened) Reject stop strings when skip_tokenizer_init is set
- [#46632](https://github.com/vllm-project/vllm/pull/46632) (Newly opened) Enable DSML structural tag for DeepSeek-V4 with auto + non-strict tools
- [#46579](https://github.com/vllm-project/vllm/pull/46579) (Newly opened) Fix KV cache memory leak when all requests finish with connector
- [#46587](https://github.com/vllm-project/vllm/pull/46587) (Newly opened) Fix test failure by using platform-aware imports
- [#46424](https://github.com/vllm-project/vllm/pull/46424) (Newly opened) Fix assert crash when prefill-reclassified-as-decode occurs with no concurrent spec tokens
- [#46426](https://github.com/vllm-project/vllm/pull/46426) (Newly opened) Fix quantization config resolution for Gemma 4 MTP draft model
</details>

<details>
<summary>Refactors (7)</summary>

- [#46022](https://github.com/vllm-project/vllm/pull/46022) (Merged) Refactor ServingTokenization entrypoint
- [#43721](https://github.com/vllm-project/vllm/pull/43721) (Merged) refactor quark_moe fp8 w/ oracle
- [#46030](https://github.com/vllm-project/vllm/pull/46030) (Merged) Responses API parser state into conversation context
- [#44514](https://github.com/vllm-project/vllm/pull/44514) (Merged) Deprecate old FP8 online MoE quantization class
- [#46647](https://github.com/vllm-project/vllm/pull/46647) (Newly opened) Move iteration logging to the frontend
- [#46405](https://github.com/vllm-project/vllm/pull/46405) (Newly opened) Remove dead kernel code
- [#46656](https://github.com/vllm-project/vllm/pull/46656) (Newly opened) New stable abi cleanup
</details>

<details>
<summary>Other (7)</summary>

- [#46511](https://github.com/vllm-project/vllm/pull/46511) (Merged) Update to log once
- [#46698](https://github.com/vllm-project/vllm/pull/46698) (Newly opened) Releases/v0.22.1
- [#46621](https://github.com/vllm-project/vllm/pull/46621) (Newly opened) Improve Triton JIT diagnostics
- [#46423](https://github.com/vllm-project/vllm/pull/46423) (Newly opened) Opt-in Inductor cudagraphs for vanilla torch.compile
- [#46665](https://github.com/vllm-project/vllm/pull/46665) (Newly opened) Use log1p to compute residual during rejection sampling
- [#46524](https://github.com/vllm-project/vllm/pull/46524) (Newly opened) Disallow DBO in multinode deployments when using the DeepEP High Throughput all2all backend
- [#46598](https://github.com/vllm-project/vllm/pull/46598) (Newly opened) Add remediation hints to MTP and PCP context-parallel errors
</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (vllm.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
