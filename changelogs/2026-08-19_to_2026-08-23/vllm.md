# vllm: PR digest (2026-08-19 to 2026-08-23)

_206 merged, 369 newly opened - source vllm-project/vllm, generated 2026-08-23T21:34:59Z_

## TL;DR
- **DeepSeek** dominated model-specific work, with a new AMX-only high-performance MLA backend for V2/V3/R1 on CPU, and extensive kernel optimizations for V4 (MegaMoE fusion, adaptive top-k).
- **Performance & Kernels**: Major wins include a massive KV-cache layout standardization, a new b12x FP4 MoE backend, and Mamba prefix caching yielding 9-25% TTFT improvements.
- **Architecture & Distributed**: Significant investments in distributed RL (P2P RDT weight sync) and in-progress work on manifest-driven streaming modelwise weight reloading.
- **Rust Frontend**: Continued maturation with new structural-tag builders, OpenAI Responses API endpoints, and in-progress `/derender` streaming capabilities.

## Most important PRs
- **[#51718](https://github.com/vllm-project/vllm/pull/51718)**: Standardizes the KV cache layout across FlashInfer, Triton, and other backends. This massive 9.7k-line refactor unifies memory management and simplifies future attention kernel integrations.
- **[#53438](https://github.com/vllm-project/vllm/pull/53438)**: Introduces manifest-driven streaming modelwise weight reloading. This newly-opened 10k-line feature enables dynamic swapping of models and weights without restarting the engine.
- **[#43375](https://github.com/vllm-project/vllm/pull/43375)**: Adds peer-to-peer RDT weight synchronization. This 8.4k-line addition significantly advances distributed reinforcement learning workflows by enabling efficient weight updates.
- **[#52616](https://github.com/vllm-project/vllm/pull/52616)**: Delivers a highly optimized AMX-only MLA backend for DeepSeek V2/V3/R1 on CPU. This drastically improves CPU inference performance for the DeepSeek model family.
- **[#52018](https://github.com/vllm-project/vllm/pull/52018)**: Adds a b12x FP4 MoE backend. This expands ultra-low precision support for Mixture of Experts, reducing memory bandwidth requirements for large MoE models.

## More changes by area

<details>
<summary>Performance (42)</summary>

- [#52606](https://github.com/vllm-project/vllm/pull/52606) [ROCm][Perf] Kimi-K3 Fused kernels for KDA prefill
- [#53294](https://github.com/vllm-project/vllm/pull/53294) Revert "[ROCm][Perf] Kimi-K3 Fused kernels for KDA prefill"
- [#53106](https://github.com/vllm-project/vllm/pull/53106) Reduce `AutoWeightsLoader` kwargs
- [#53152](https://github.com/vllm-project/vllm/pull/53152) [K3 Perf] Fuse MXFP4 top-k finalization into latent-tail, ~5% E2E latency reduction
- [#52925](https://github.com/vllm-project/vllm/pull/52925) [Core][Multimodal] Skip redundant placeholder scan when token match succeeds
- [#52882](https://github.com/vllm-project/vllm/pull/52882) [ROCm][Perf] Optimize DeepSeek V4 C4A top-k with AITER
- [#52789](https://github.com/vllm-project/vllm/pull/52789) [Perf] Support internal prefill checkpoints for Mamba prefix caching, 9%~25% TTFT improvement
- [#51885](https://github.com/vllm-project/vllm/pull/51885) [Elastic EP] Reduce eager-mode reconfiguration downtime
- [#43018](https://github.com/vllm-project/vllm/pull/43018) [ROCm] Cpu offload for ROCm 7.13+ to align the hipMemcpyBatchAsync params and perf in 7.14x
- [#52737](https://github.com/vllm-project/vllm/pull/52737) [ROCm][Perf] Fuse DeepSeek-V4 mHC post/pre and RMSNorm with AITER
- [#52827](https://github.com/vllm-project/vllm/pull/52827) [MM] Keep more metadata tensors on CPU
- [#53196](https://github.com/vllm-project/vllm/pull/53196) [Kimi K3][Perf] Export FlashKDA checkpoints in one packed call
- [#52041](https://github.com/vllm-project/vllm/pull/52041) [Core] Skip broadcasting mm tensor data to workers for prefix-cache-covered items
- [#52823](https://github.com/vllm-project/vllm/pull/52823) [DSv4 Perf] Adaptive topk width for dsv4, making #50004 back
- [#53267](https://github.com/vllm-project/vllm/pull/53267) [Performance][MRV2] Fuse vocab-parallel LM head projection for small-K prompt logprobs
- [#53112](https://github.com/vllm-project/vllm/pull/53112) [perf][MoE] flashinfer fp4 shared expert fusion
- [#53094](https://github.com/vllm-project/vllm/pull/53094) [ROCm][Perf] Fuse DSA indexer QK preprocessing with AITER
- [#53184](https://github.com/vllm-project/vllm/pull/53184) [Perf][Humming] Integrate fused SwiGLU FP8 quantization for W2
- [#53301](https://github.com/vllm-project/vllm/pull/53301) [ROCm][Perf] Reuse graph-stable attention metadata across Kimi-K3 cache groups
- [#53161](https://github.com/vllm-project/vllm/pull/53161) [ROCm][Perf][DeepSeek V4] Fuse native FP8 shared expert with MXFP4 routed experts
- [#52901](https://github.com/vllm-project/vllm/pull/52901) [ROCm][Perf] Add AITER gated QKV + RoPE + kv-cache compile fusion
- [#53154](https://github.com/vllm-project/vllm/pull/53154) [ROCm][Quant][Kimi-K3] Fuse MXFP4 activation quant into Kimi-K3 attention epilogues
- [#53335](https://github.com/vllm-project/vllm/pull/53335) [ROCm][Perf][Attention] Add FlyDSL gfx950 prefill attention backend
- [#53169](https://github.com/vllm-project/vllm/pull/53169) WIP: Reduce multimodal payload in token-in/token-out by deferring pixel_values
- [#53090](https://github.com/vllm-project/vllm/pull/53090) [Perf][Spec Decode] Fuse target temperature in rejection sampler
- [#52963](https://github.com/vllm-project/vllm/pull/52963) [ROCm][Perf][MiniMax-M3] Optimize sparse GQA prefill attention
- [#53448](https://github.com/vllm-project/vllm/pull/53448) [ROCm][Perf] Speed up the lightning indexer's score and top-k
- [#53027](https://github.com/vllm-project/vllm/pull/53027) [Performance][Model] Fuse GLM indexer attention projections
- [#52849](https://github.com/vllm-project/vllm/pull/52849) [ROCm][PERF] Enable AITER PA gluon decode for MiniMax-M3 MTP and dense layers
- [#53446](https://github.com/vllm-project/vllm/pull/53446) [Kernel][Perf] Add Hopper (SM90) tuned config for batch-invariant persistent matmul
- [#53247](https://github.com/vllm-project/vllm/pull/53247) [Kernel][Perf] Per-architecture tuned configs for batch-invariant persistent matmul
- [#53410](https://github.com/vllm-project/vllm/pull/53410) [Perf] TurboQuant: run spec-decode verify batches as decodes with FULL cudagraphs
- [#53318](https://github.com/vllm-project/vllm/pull/53318) [Perf] Tune FlashInfer all-reduce selection on SM103
- [#53166](https://github.com/vllm-project/vllm/pull/53166) [kimik3][ROCm][Perf] Fuse MLA chunked-context gather on AITER
- [#53464](https://github.com/vllm-project/vllm/pull/53464) [Perf] Improve performance for BGE-M3 MRV2 pooling token-ID metadata
- [#52993](https://github.com/vllm-project/vllm/pull/52993) [K3] Optimize K3 recover ssm kernel times
- [#52983](https://github.com/vllm-project/vllm/pull/52983) [ROCm][Perf] W4A16: magic-bias dequant + scale hoist for gfx90a, gated on BLOCK_M <= 16
- [#53070](https://github.com/vllm-project/vllm/pull/53070) [Kernel][Perf] Support DSpark K=8 in fused GDN MTP decode
- [#52875](https://github.com/vllm-project/vllm/pull/52875) [Perf][Frontend] Render plain completion stream deltas from a template
- [#53259](https://github.com/vllm-project/vllm/pull/53259) [ROCm][Perf] Add `gelu_tanh` activation to AITER fp8 fmoe
- [#53463](https://github.com/vllm-project/vllm/pull/53463) [Kernel][Perf] Route non-spec GDN decode through the fused CUDA kernel
- [#52984](https://github.com/vllm-project/vllm/pull/52984) [ROCm][Perf] W4A16 gfx90a: extend the narrow-tile rung to M<=16

</details>

<details>
<summary>Kernels & attention (34)</summary>

- [#52816](https://github.com/vllm-project/vllm/pull/52816) [Spec Decode] DFlash2: local convolution + candidate selector
- [#53053](https://github.com/vllm-project/vllm/pull/53053) [Kimi-K3] Extend GEMM-RS to GEMM-AR
- [#53040](https://github.com/vllm-project/vllm/pull/53040) [DSV4][Kernel] Fuse shared experts into MegaMoE
- [#52836](https://github.com/vllm-project/vllm/pull/52836) Revert DSv4 eager workspace reuse
- [#46514](https://github.com/vllm-project/vllm/pull/46514) [Attention][MLA] FlashMLA sparse: DCP on the fp8_ds_mla mixed-batch path + MTP
- [#52204](https://github.com/vllm-project/vllm/pull/52204) [Kernel] Add FlashInfer TRTLLM MXFP8 linear backend
- [#52987](https://github.com/vllm-project/vllm/pull/52987) Revert "[Kernel] Gemma-4 FA4 FP8 Kernel"
- [#52217](https://github.com/vllm-project/vllm/pull/52217) [Attention] Vectorize sparse MLA mask loads
- [#50400](https://github.com/vllm-project/vllm/pull/50400) [Kernel][Kimi] fused vision q/k roper kernel
- [#52795](https://github.com/vllm-project/vllm/pull/52795) [Spec Decode] Enable adaptive verification on DSv4 + sm90
- [#52078](https://github.com/vllm-project/vllm/pull/52078) [Attention] Avoid redundant mask compute in GDN metadata build
- [#52775](https://github.com/vllm-project/vllm/pull/52775) [Kernel] SM120: stop routing misaligned-M blockwise FP8 GEMMs to the small-M swapAB config
- [#53289](https://github.com/vllm-project/vllm/pull/53289) Helion KDA backend port from sglang
- [#53060](https://github.com/vllm-project/vllm/pull/53060) turboquant decode attetnion optimization
- [#53202](https://github.com/vllm-project/vllm/pull/53202) [Kernel] Default unquantized BF16 linear to FlashInfer mm_bf16 and drop the CuTe skinny GEMM
- [#52928](https://github.com/vllm-project/vllm/pull/52928) [Mamba] Add FlashInfer ReplaySSM support for MTP
- [#53173](https://github.com/vllm-project/vllm/pull/53173) [glm] [pcp] fuse norm rope with pcp cache gather
- [#53475](https://github.com/vllm-project/vllm/pull/53475) [ROCm] Extend fused KDA decode to DSpark spec (num_spec<=2)
- [#52968](https://github.com/vllm-project/vllm/pull/52968) attn res fusion + stream enablement
- [#53384](https://github.com/vllm-project/vllm/pull/53384) [Kernel][ROCm] Flash-decoding sequence partitioning for the Triton paged decode path
- [#53383](https://github.com/vllm-project/vllm/pull/53383) [Kernel][ROCm] Partition the cached-context scan for short-query attention (spec-decode verify)
- [#53426](https://github.com/vllm-project/vllm/pull/53426) [Core][Spec Decode] Opt-in skip of the K=0 draft sync forward (speculative_config, default off)
- [#53396](https://github.com/vllm-project/vllm/pull/53396) [K3] Support DS conv-state layout in fused KDA decode kernel
- [#52980](https://github.com/vllm-project/vllm/pull/52980) [SM100] Hdim 256 optimized
- [#53427](https://github.com/vllm-project/vllm/pull/53427) [Spec Decode] Support MTP with PCP in the V2 GPU runner
- [#53168](https://github.com/vllm-project/vllm/pull/53168) [Kernel][Kimi] Fuse MoonViT Q/K complex RoPE
- [#53147](https://github.com/vllm-project/vllm/pull/53147) [Kernel][Gemma4] Prune Triton sliding-window tiles for multimodal prefixes
- [#52988](https://github.com/vllm-project/vllm/pull/52988) [Spec decode] Support variable-length decode for Kimi-K3 adaptive ver
- [#53001](https://github.com/vllm-project/vllm/pull/53001) [ROCm][Spec Decode] Add Aiter MLA decode support non-causal draft block
- [#53465](https://github.com/vllm-project/vllm/pull/53465) [DCP] Add DCP qrep to GLM-5.2 flat model definition
- [#53007](https://github.com/vllm-project/vllm/pull/53007) add option to select different backend for sliding window layers
- [#53214](https://github.com/vllm-project/vllm/pull/53214) [Spec Decode] Support single-file checkpoints for target and draft models
- [#53388](https://github.com/vllm-project/vllm/pull/53388) [Feature][Spec] Support disabling trailing prefix-cache block dropping
- [#53036](https://github.com/vllm-project/vllm/pull/53036) [Attention][Spec Decode] Enable varlen Mamba2 decode for adaptive verification

</details>

<details>
<summary>MoE & quantization (14)</summary>

- [#50501](https://github.com/vllm-project/vllm/pull/50501) [XPU][INC] Add int4 w4a8 (dynamic int8 activation) backend for INC linear layers
- [#48918](https://github.com/vllm-project/vllm/pull/48918) [CT] Support Humming for WNA16 MoE
- [#37835](https://github.com/vllm-project/vllm/pull/37835) [ROCm] Add UE8M0 scale packing for Triton silu_mul_quant
- [#52962](https://github.com/vllm-project/vllm/pull/52962) [Mamba] Support quantized FlashInfer ReplaySSM state cache
- [#53065](https://github.com/vllm-project/vllm/pull/53065) [XPU][MoE] Tune Triton fused MoE for Intel XPU
- [#53231](https://github.com/vllm-project/vllm/pull/53231) [ROCm] TurboQuant KV cache support for Gemma 4
- [#53014](https://github.com/vllm-project/vllm/pull/53014) [Kernel] add Flashinfer cutedsl w4a16 linear
- [#53097](https://github.com/vllm-project/vllm/pull/53097) [ROCm][Quantization][MOE] Enable fused shared experts for block-quantized FP8
- [#53222](https://github.com/vllm-project/vllm/pull/53222) [ROCm] Add opt-in token chunking for the AITER fused-MoE experts call
- [#53068](https://github.com/vllm-project/vllm/pull/53068) [ROCm][Quantization] Implement Fp8Config shared-expert FSE compatibility check
- [#52890](https://github.com/vllm-project/vllm/pull/52890) restore 2/3-bit CUDA support in AutoRound format
- [#53101](https://github.com/vllm-project/vllm/pull/53101) [Model] Add FP8 quantization support for ModernBERT
- [#53319](https://github.com/vllm-project/vllm/pull/53319) [Kernel] Add NVFP4 support to the torch linear backend
- [#53162](https://github.com/vllm-project/vllm/pull/53162) [Quantization][XPU] Enable int8_w8a8 per-token MoE on the Triton backend for XPU

</details>

<details>
<summary>Model support (13)</summary>

- [#53272](https://github.com/vllm-project/vllm/pull/53272) Remove native Hunyuan V1 and VL implementations
- [#53296](https://github.com/vllm-project/vllm/pull/53296) Revert "Remove native Hunyuan V1 and VL implementations"
- [#52560](https://github.com/vllm-project/vllm/pull/52560) [Model] Add Qwen3-Omni DSpark support
- [#52861](https://github.com/vllm-project/vllm/pull/52861) [Model][NVIDIA] Route DSA models to the CUDA non-compiled path
- [#52706](https://github.com/vllm-project/vllm/pull/52706) [Model] Add GraniteSWA and GraniteMoeSWA via existing Granite
- [#52209](https://github.com/vllm-project/vllm/pull/52209) Add routed expert loading for gpt-oss
- [#53132](https://github.com/vllm-project/vllm/pull/53132) Support kimi k3 nvfp4 checkpoint
- [#52948](https://github.com/vllm-project/vllm/pull/52948) [Model] Support bidirectional (encoder-only) attention for DeepSeek e…
- [#51498](https://github.com/vllm-project/vllm/pull/51498) [Model] Add tower and connector LoRA support for LFM2-VL
- [#52929](https://github.com/vllm-project/vllm/pull/52929) Add NemotronH_Omni_Reasoning_V3 as a supported Nemotron architecture
- [#53373](https://github.com/vllm-project/vllm/pull/53373) [Model] Add Spark3 Model
- [#53052](https://github.com/vllm-project/vllm/pull/53052) Support EAGLE3 for Sarvam
- [#52977](https://github.com/vllm-project/vllm/pull/52977) [Model][Llama] Support hidden_act variants in gated MLP

</details>

<details>
<summary>Parallelism & scheduling (21)</summary>

- [#52466](https://github.com/vllm-project/vllm/pull/52466) [KV Connector] Add decode offloading to Mooncake Store consumers
- [#50723](https://github.com/vllm-project/vllm/pull/50723) [Core][RL] Support sparse checkpoint updates through native weight loaders
- [#49532](https://github.com/vllm-project/vllm/pull/49532) [XPU] Support EC connector KV Offloading on XPU
- [#52998](https://github.com/vllm-project/vllm/pull/52998) [Distributed] Enable FlashInfer all-reduce by default
- [#53348](https://github.com/vllm-project/vllm/pull/53348) [Feature] Container Snapshot Support
- [#53350](https://github.com/vllm-project/vllm/pull/53350) [Feature] Container Snapshot Support
- [#53129](https://github.com/vllm-project/vllm/pull/53129) [KV Connector] Support heterogeneous TP sharing in Mooncake Store Connector
- [#53360](https://github.com/vllm-project/vllm/pull/53360) [KV Connector][NIXL] Support pipeline-parallel producers on the pull path (incl. hybrid-Mamba)
- [#53422](https://github.com/vllm-project/vllm/pull/53422) [Feature] Add PCP O-Proj tensor parallelism
- [#53205](https://github.com/vllm-project/vllm/pull/53205) [Mooncake][PD] Support DCP transfer for MLA/GQA models
- [#52863](https://github.com/vllm-project/vllm/pull/52863) [Kernel][PCP] Publish replicated KV updates through PyTorch symmetric memory
- [#52856](https://github.com/vllm-project/vllm/pull/52856) [XPU] [AsyncTP] Support FP8 block quant AsyncTP collective fusion
- [#53022](https://github.com/vllm-project/vllm/pull/53022) [Model][EPLB] Add static expert maps for DeepSeek V4
- [#53265](https://github.com/vllm-project/vllm/pull/53265) [3/N][KV Connector][NIXL] Support per-region transfer geometry
- [#53133](https://github.com/vllm-project/vllm/pull/53133) Add multi-path sharding and aligned direct I/O to FS offloading
- [#53263](https://github.com/vllm-project/vllm/pull/53263) [1/N][KV Connector][NIXL] Stage host KV reads through device memory
- [#52859](https://github.com/vllm-project/vllm/pull/52859) [KV Connector][Observability] Add lifecycle tracing for NIXL push and pull
- [#53102](https://github.com/vllm-project/vllm/pull/53102) [Feature][Spec Decode] Carry auxiliary state across PP stages
- [#53324](https://github.com/vllm-project/vllm/pull/53324) [KV Connector] Support MooncakeStore with hybrid DCP prefix caching
- [#53067](https://github.com/vllm-project/vllm/pull/53067) [KV Connector] Add scheduler context for lazy block access
- [#53264](https://github.com/vllm-project/vllm/pull/53264) [2/N][KV Connector] Identify externally transferable KV cache groups

</details>

<details>
<summary>Hardware & arch (4)</summary>

- [#53201](https://github.com/vllm-project/vllm/pull/53201) [XPU] follow cuda path for mrope on XPU
- [#53300](https://github.com/vllm-project/vllm/pull/53300) [CPU][GDN] Support NIXL DS convolution-state layout
- [#53153](https://github.com/vllm-project/vllm/pull/53153) [hw-agnostic] Implemented plumbing to support OOT plugins
- [#52917](https://github.com/vllm-project/vllm/pull/52917) [Core][Hardware][Arm][Intel] Adaptive spin grace + bounded arch waits (aarch64 WFET, x86 WAITPKG) for shm_broadcast

</details>

<details>
<summary>API & serving (33)</summary>

- [#46701](https://github.com/vllm-project/vllm/pull/46701) [Core][V1] Support trace_decode_token_ids for deterministic decode replay
- [#53054](https://github.com/vllm-project/vllm/pull/53054) [Rust Frontend] Add HY3 unified parser and local XGrammar structural-tag builder
- [#48915](https://github.com/vllm-project/vllm/pull/48915) [Frontend][Core][Spec Decode] Per-request acceptance stats in OpenAI API responses
- [#49811](https://github.com/vllm-project/vllm/pull/49811) [Feature][Model Runner V2] Support extract_hidden_states speculation
- [#53044](https://github.com/vllm-project/vllm/pull/53044) [Rust Frontend] Support `--generation-config vllm`
- [#52473](https://github.com/vllm-project/vllm/pull/52473) using existing uvicorn configuration for dp supervisor
- [#53213](https://github.com/vllm-project/vllm/pull/53213) [Pooling] Report input throughput for batched requests
- [#53308](https://github.com/vllm-project/vllm/pull/53308) Forward Anthropic vllm_xargs to sampling params
- [#48290](https://github.com/vllm-project/vllm/pull/48290) [ModelRunner v2] Enable MRV2 for pooling models by default
- [#52867](https://github.com/vllm-project/vllm/pull/52867) [Pooling] Use semantic task validation errors
- [#53204](https://github.com/vllm-project/vllm/pull/53204) [Rust Frontend][RL]: report engine world size over gRPC
- [#53127](https://github.com/vllm-project/vllm/pull/53127) [Misc] Don't allow language-model-only used with encoder CG together
- [#40834](https://github.com/vllm-project/vllm/pull/40834) [Core] Add dynamo_timed tracing for print_readable
- [#53419](https://github.com/vllm-project/vllm/pull/53419) [Rust Frontend] /derender: streaming derender + two-process e2e test (phase 3/3)
- [#53380](https://github.com/vllm-project/vllm/pull/53380) [Rust Frontend] Add OpenAI Responses API endpoint
- [#53418](https://github.com/vllm-project/vllm/pull/53418) [Rust Frontend] /derender: reasoning and tool-call parsing (phase 2/3)
- [#53223](https://github.com/vllm-project/vllm/pull/53223) [Rust Frontend] Add /derender endpoints: detokenization and state (phase 1/3)
- [#52896](https://github.com/vllm-project/vllm/pull/52896) [Rust Frontend] Add Anthropic Messages API request surface and count_tokens (PR 1/3)
- [#52876](https://github.com/vllm-project/vllm/pull/52876) Add separate post-thinking sampling parameters
- [#53135](https://github.com/vllm-project/vllm/pull/53135) [Frontend] Defer runtime imports until CLI dispatch
- [#53183](https://github.com/vllm-project/vllm/pull/53183) [Model Runner V2] Use MRV2 for all models by default
- [#52900](https://github.com/vllm-project/vllm/pull/52900) [Rust Frontend] Add LFM2 tool parser
- [#52910](https://github.com/vllm-project/vllm/pull/52910) [Rust Frontend] Attribute decoded text to tokens
- [#53306](https://github.com/vllm-project/vllm/pull/53306) [Model Runner V2] Reserve CUDA graph memory
- [#53218](https://github.com/vllm-project/vllm/pull/53218) [Rust Frontend] Align OpenAI request and response edge cases
- [#53219](https://github.com/vllm-project/vllm/pull/53219) Add Cohere ChatV2 render endpoint
- [#53187](https://github.com/vllm-project/vllm/pull/53187) [Frontend] Return prompt metadata from /inference/v1/generate
- [#52946](https://github.com/vllm-project/vllm/pull/52946) [Rust Frontend] Add Step3p5 tool parser
- [#52864](https://github.com/vllm-project/vllm/pull/52864) [Frontend][RL] Add structured sleep responses and weight info tests
- [#53099](https://github.com/vllm-project/vllm/pull/53099) [Parser] Move structural-tag capabilities into parser engines
- [#53082](https://github.com/vllm-project/vllm/pull/53082) [Core] Make sleep a pure memory-state transition
- [#53423](https://github.com/vllm-project/vllm/pull/53423) [Feature] Add first-class KV hints request envelope for programmatic KV management
- [#53198](https://github.com/vllm-project/vllm/pull/53198) [Metrics] Expose per-request remote KV wait time

</details>

<details>
<summary>Tests (39)</summary>

- [#51827](https://github.com/vllm-project/vllm/pull/51827) [3/N] Harden Transformers modelling backend multi-modal path
- [#51570](https://github.com/vllm-project/vllm/pull/51570) [Rust][Benchmark] Load HF datasets from parquet shards via hf-hub, fixing truncated-cache sampling
- [#51592](https://github.com/vllm-project/vllm/pull/51592) [Rust][Benchmark] Align speed-bench CLI flags with Python and add flag parity test
- [#41100](https://github.com/vllm-project/vllm/pull/41100) [ROCm][CI] Extended Fused MoE and FP8 MoE test support
- [#51968](https://github.com/vllm-project/vllm/pull/51968) [XPU][Tests] Make tests device-agnostic
- [#53189](https://github.com/vllm-project/vllm/pull/53189) [Test] Add focused hybrid MTP prefix-cache regressions
- [#53023](https://github.com/vllm-project/vllm/pull/53023) [CI] Fix MultiConnector accuracy test lifecycle
- [#52313](https://github.com/vllm-project/vllm/pull/52313) [LoRA] Avoid false target matches for unsupported module types
- [#52697](https://github.com/vllm-project/vllm/pull/52697) [EPD] Allow KV consumers to omit MM embeddings
- [#50382](https://github.com/vllm-project/vllm/pull/50382) [DCP] Default query replication for GLM sparse attention
- plus 29 more minor test updates

</details>

<details>
<summary>CI & build (29)</summary>

- [#52976](https://github.com/vllm-project/vllm/pull/52976) [CI][ROCm] Standardize AMD test job labels by device
- [#51459](https://github.com/vllm-project/vllm/pull/51459) [CI] Fix and extend PR/issue auto-labeling
- [#52572](https://github.com/vllm-project/vllm/pull/52572) [CI] replace shellcheck script with shellcheck-py hook
- [#52672](https://github.com/vllm-project/vllm/pull/52672) [XPU] upgrade requirements/test/xpu.txt
- [#52892](https://github.com/vllm-project/vllm/pull/52892) [Rust Frontend] Replace external `protoc` with pure Rust lib `protox`
- [#53025](https://github.com/vllm-project/vllm/pull/53025) [ROCm][CI] Stabilize MI355 FusedMoE test group
- [#51630](https://github.com/vllm-project/vllm/pull/51630) [XPU][CI]Add more cases in intel GPU CI and reorganize to align non-xpu part
- [#53117](https://github.com/vllm-project/vllm/pull/53117) [CI/Build][ROCm] Run the TileLang HIP symbol checks in their own interpreter
- [#52547](https://github.com/vllm-project/vllm/pull/52547) [CI][AMD] Honor single-node Docker workload timeout
- [#53172](https://github.com/vllm-project/vllm/pull/53172) [CI][Docker] Pin remaining manylinux builder images
- plus 19 more minor CI updates

</details>

<details>
<summary>Docs (7)</summary>

- [#39082](https://github.com/vllm-project/vllm/pull/39082) [Docs] document cache salting for prefix cache timing side-channel mitigation
- [#52726](https://github.com/vllm-project/vllm/pull/52726) [Doc] Update Gaudi HPU committers
- [#53098](https://github.com/vllm-project/vllm/pull/53098) [Docs] Use incremental builds for C++ changes in `AGENTS.md`
- [#52955](https://github.com/vllm-project/vllm/pull/52955) Sm89
- [#53325](https://github.com/vllm-project/vllm/pull/53325) [WIP] Vllm recipes tool improve
- [#53045](https://github.com/vllm-project/vllm/pull/53045) [RFC][Reload] Define V1/V2 reload and streaming quantization units
- [#52967](https://github.com/vllm-project/vllm/pull/52967) docs: Add NIXL connector metrics aggregation documentation

</details>

<details>
<summary>Bugfixes (153)</summary>

- [#52175](https://github.com/vllm-project/vllm/pull/52175) Fix Cohere ChatV2 citation and tool handling issues
- [#51665](https://github.com/vllm-project/vllm/pull/51665) Fix weight tying
- [#49688](https://github.com/vllm-project/vllm/pull/49688) [Bugfix][CPU] Enable C++ causal_conv1d GDN path and float32 SSM cache on non-AMX AVX-512BF16 CPUs
- [#53460](https://github.com/vllm-project/vllm/pull/53460) [Model] Fix KV cache layout and optimize Dots3 NOTE Omni encoders
- [#51824](https://github.com/vllm-project/vllm/pull/51824) [Bugfix] vLLM crashes at startup when DeepEP v2 is used with `--enforce-eager` wiht TRTLLM Bf16
- [#51863](https://github.com/vllm-project/vllm/pull/51863) [Bugfix][Benchmark] Check readiness before tokenizer init in rust vllm-bench
- [#52704](https://github.com/vllm-project/vllm/pull/52704) [Bugfix][Quantization] Fix OCP MX MoE emulation silently skipping mxfp6 activation QDQ
- [#52874](https://github.com/vllm-project/vllm/pull/52874) [Bugfix][Model] Mistral3: fix image placeholder grid for processor size overrides
- [#52779](https://github.com/vllm-project/vllm/pull/52779) [Bugfix][KV Connector][NIXL] Support PCP producers
- [#52766](https://github.com/vllm-project/vllm/pull/52766) Fix Transformers modelling backend `RMSNormFuser.fuse` performance
- [#42376](https://github.com/vllm-project/vllm/pull/42376) [Bugfix][Spec Decode]Preserve user --speculative-config overrides for speculators-format models
- [#53381](https://github.com/vllm-project/vllm/pull/53381) [Mypy Fix] Mypy fix for "vllm/model_executor/models/[eE][fF]"
- [#53240](https://github.com/vllm-project/vllm/pull/53240) [Bugfix][R3] Unwrap UniformTypeKVCacheSpecs when selecting the routed-experts KV group
- [#45807](https://github.com/vllm-project/vllm/pull/45807) fix: report stop_sequence stop_reason in Anthropic Messages API
- [#47272](https://github.com/vllm-project/vllm/pull/47272) [Bugfix][Core] Reserve the KV null block when validating max_model_len
- plus 138 more minor bugfixes

</details>

<details>
<summary>Refactors (12)</summary>

- [#53275](https://github.com/vllm-project/vllm/pull/53275) [MM] Simplify `_apply_hf_processor_main`
- [#52839](https://github.com/vllm-project/vllm/pull/52839) [refactor] consolidate cp attn ops
- [#53372](https://github.com/vllm-project/vllm/pull/53372) [MM] Simplify prompt updates: replace `PromptSeq` with `list[int]`
- [#52131](https://github.com/vllm-project/vllm/pull/52131) [Frontend] Move api_server.py out openai folder
- [#53093](https://github.com/vllm-project/vllm/pull/53093) [MM] Remove text components from ProcessorInputs
- [#53064](https://github.com/vllm-project/vllm/pull/53064) [Refactor] Remove InputPreprocessor
- [#53139](https://github.com/vllm-project/vllm/pull/53139) [Cleanup][MLA] Remove FlashInfer DSpark DCP support
- [#52281](https://github.com/vllm-project/vllm/pull/52281) [ROCm] Give EngineCore cleanup grace after request abort
- [#53176](https://github.com/vllm-project/vllm/pull/53176) [Refactor][Model Runner V2][Multimodal] Move the encoder-only path out of the shared runner
- [#53385](https://github.com/vllm-project/vllm/pull/53385) [MM] Remove renderer_applies_updates flag
- [#53021](https://github.com/vllm-project/vllm/pull/53021) [Model] Remove unused DeepseekV32Indexer forward
- [#52958](https://github.com/vllm-project/vllm/pull/52958) [Quantization][Refactor][1/N] Adopt `QuantKey` in `QuarkConfig` and methods, relying on `weight_quant_key`, `act_quant_key` for quant method dispatch

</details>

<details>
<summary>Other (4)</summary>

- [#51781](https://github.com/vllm-project/vllm/pull/51781) [Platform] Fill in the missing backend parameter for torch.compile
- [#53364](https://github.com/vllm-project/vllm/pull/53364) [MM] Address comments on [#53275](https://github.com/vllm-project/vllm/pull/53275)
- [#53175](https://github.com/vllm-project/vllm/pull/53175) Resubmit PR 48666
- [#52886](https://github.com/vllm-project/vllm/pull/52886) [Rust Frontend] Recover incomplete Kimi K3 calls at outer boundaries

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (vllm.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 0017688ad271fa4cea5d4a6f6a9a4692420f2a81b06ea346498ab078ab38f007 -->
