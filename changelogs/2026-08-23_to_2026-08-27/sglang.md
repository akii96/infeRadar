# sglang: PR digest (2026-08-23 to 2026-08-27)

_290 merged, 404 newly opened - source sgl-project/sglang, generated 2026-08-27T20:07:20Z_

## TL;DR
- **Model focus:** DeepSeek (V4), MiniMax (H3, M3), and GLM (5.3-Flash) saw the most activity, alongside major newly-opened work for Qwen 3.8 Flash Next.
- **Performance & Kernels:** Significant MoE and attention kernel work, including the DeepEPv2 (ElasticBuffer) MoE A2A backend, FlashInfer EXTEND tuning, and AMD ROCm MegaMoE paths.
- **Features:** Beam search support was merged, and major architectural work is underway for streamed LoRA weight updates and unified radix tree backends.
- **Hardware:** Intel XPU received massive updates for DeepSeek V4, while AMD ROCm and Ascend NPU saw continued optimization and model enablement.

## Most important PRs
- **[#36497](https://github.com/sgl-project/sglang/pull/36497)** (Newly opened): Introduces support for Qwen 3.8 Flash Next, bringing the latest Qwen architecture to the engine with comprehensive backend support.
- **[#36507](https://github.com/sgl-project/sglang/pull/36507)** (Newly opened): Adds comprehensive support for GLM-5.3-Flash, including Triton and FlashInfer backends, speculative decoding, and multimodal capabilities.
- **[#36588](https://github.com/sgl-project/sglang/pull/36588)**: Rebases the `intel_dev` branch and adds extensive Intel XPU optimizations for DeepSeek V4, touching almost every component.
- **[#31626](https://github.com/sgl-project/sglang/pull/31626)**: Implements beam search support, a major feature addition for structured output and speculative decoding workflows.
- **[#35634](https://github.com/sgl-project/sglang/pull/35634)**: Adds the DeepEPv2 (ElasticBuffer) MoE all-to-all backend, significantly improving MoE routing performance via Triton.

## More changes by area

<details>
<summary>Performance (15)</summary>

- [#35735](https://github.com/sgl-project/sglang/pull/35735) Split the custom all-reduce communicator into push/pull planes
- [#33871](https://github.com/sgl-project/sglang/pull/33871) Reduce idle DP work in breakable prefill CUDA graphs
- [#36219](https://github.com/sgl-project/sglang/pull/36219) Tune FlashInfer EXTEND for DP prefill
- [#34066](https://github.com/sgl-project/sglang/pull/34066) Batch lazy-compaction mapping lookup for unified memory
- [#36004](https://github.com/sgl-project/sglang/pull/36004) Use full 1024-thread block for indexer top-k on ROCm
- [#36397](https://github.com/sgl-project/sglang/pull/36397) Tune custom all reduce v2 for sm_107
- [#36652](https://github.com/sgl-project/sglang/pull/36652) TRTLLM Attention: Accuracy + Perf Improvements for DSv4
- [#36145](https://github.com/sgl-project/sglang/pull/36145) Add the B300 SP-collective tuning table for Kimi-K3
- [#36411](https://github.com/sgl-project/sglang/pull/36411) Optimize repeated Qwen-VL multimodal serving
- [#36501](https://github.com/sgl-project/sglang/pull/36501) Fuse static FP8 quantization into FlashInfer allreduce
- [#36103](https://github.com/sgl-project/sglang/pull/36103) Sample next tokens from temperature-scaled logits without materializing full-vocab probs
- [#36065](https://github.com/sgl-project/sglang/pull/36065) Split mixed GDN prefill and decode kernels
- [#36305](https://github.com/sgl-project/sglang/pull/36305) Unify q8kv8 sparse-prefill topk_length source with the bf16 path
- [#36041](https://github.com/sgl-project/sglang/pull/36041) Honor explicit workload caps when sizing hybrid cache
- [#36505](https://github.com/sgl-project/sglang/pull/36505) Page-level KV view for gfx950 fp8 page-64 asm prefill

</details>

<details>
<summary>Kernels & attention (49)</summary>

- [#32162](https://github.com/sgl-project/sglang/pull/32162) Support hisparse multi-step swap io kernel
- [#36233](https://github.com/sgl-project/sglang/pull/36233) Add CUDA 13.4 container for initial Rubin support
- [#36258](https://github.com/sgl-project/sglang/pull/36258) Attention-FFN Disaggregation Experimental for NPU
- [#36330](https://github.com/sgl-project/sglang/pull/36330) Optimize Qwen3.5 MTP unified attention on gfx950
- [#36063](https://github.com/sgl-project/sglang/pull/36063) Reuse SRT quantization contracts and MXFP8 kernels for Diffusion
- [#35995](https://github.com/sgl-project/sglang/pull/35995) Fuse LongCat-Image QKNorm and interleaved RoPE
- [#36003](https://github.com/sgl-project/sglang/pull/36003) Skip reserved writes in MLA KV cache
- [#35947](https://github.com/sgl-project/sglang/pull/35947) Publish gated DSV4 DFLASH-family target-prefill read completion
- [#35969](https://github.com/sgl-project/sglang/pull/35969) Accelerate LingBot Video RMSNorm in quality=high
- [#35981](https://github.com/sgl-project/sglang/pull/35981) Flatten Wan VAE RMSNorm row addressing
- [#35676](https://github.com/sgl-project/sglang/pull/35676) Adapt sgl-kernel-npu ops for DeepSeek-V4
- [#35454](https://github.com/sgl-project/sglang/pull/35454) Harden FlashAttention CUDA graph metadata bounds
- [#36571](https://github.com/sgl-project/sglang/pull/36571) Fuse Cosmos3 Nano T2I attention on Hopper
- [#36592](https://github.com/sgl-project/sglang/pull/36592) Fuse Wan FFN GELU epilogue
- [#36009](https://github.com/sgl-project/sglang/pull/36009) Fix Hunyuan QKV pack indexing at production video shapes
- [#36176](https://github.com/sgl-project/sglang/pull/36176) Share the warp vectorized copy and enforce its alignment
- [#36446](https://github.com/sgl-project/sglang/pull/36446) Selectively dequantize FP8 KV for BF16 DSA prefill
- [#36059](https://github.com/sgl-project/sglang/pull/36059) Add native H16 CuTe sparse prefill backend for DSV4
- [#36340](https://github.com/sgl-project/sglang/pull/36340) Add SM100 FP4 KV Cache support
- [#36038](https://github.com/sgl-project/sglang/pull/36038) Fix NVFP4 speculative decoding with TRTLLM MHA
- [#36294](https://github.com/sgl-project/sglang/pull/36294) Share replicated-Q weight storage for Kimi-K3
- [#36546](https://github.com/sgl-project/sglang/pull/36546) Run the sparse prefill main attention through AITER Gluon paged attention for MiniMax-M3
- [#36349](https://github.com/sgl-project/sglang/pull/36349) Migrate FlyDSL fused norm kernels to the v0.3.0 stable API
- [#36283](https://github.com/sgl-project/sglang/pull/36283) Optimize MiniMax sparse KV page lookups
- [#36685](https://github.com/sgl-project/sglang/pull/36685) Add optional aiter fp8 ASM MLA decode for the unified_kv path
- [#36689](https://github.com/sgl-project/sglang/pull/36689) Support prefill context parallelism with interleave and zi for DSv4 on NPU
- [#36502](https://github.com/sgl-project/sglang/pull/36502) Fuse Helios paired transposed RoPE
- [#36087](https://github.com/sgl-project/sglang/pull/36087) Dequantize only referenced FP8 KV pages in fa3_mla
- [#36304](https://github.com/sgl-project/sglang/pull/36304) Enable fused KDA decode for TP4 on Kimi-K3
- [#36206](https://github.com/sgl-project/sglang/pull/36206) Enable KDA projection fusion for DP attention on Kimi-K3
- [#36298](https://github.com/sgl-project/sglang/pull/36298) Fix whisper xpu varlen encoder decoder
- [#36644](https://github.com/sgl-project/sglang/pull/36644) Fix FP8 KV cache support in QSA for Qwen3.8
- [#36680](https://github.com/sgl-project/sglang/pull/36680) Optimize Qwen-Image TP collectives and attention
- [#36527](https://github.com/sgl-project/sglang/pull/36527) Share the sparse index top-k across layers and reuse the decode top-k buffer for MiniMax-M3
- [#36267](https://github.com/sgl-project/sglang/pull/36267) Optimize Qwen3.5 GDN prefill projection layouts
- [#36560](https://github.com/sgl-project/sglang/pull/36560) Wave64 histogram-select decode top-k, and raise kMaxNumBlocks for CUDA graphs for MiniMax-M3
- [#36534](https://github.com/sgl-project/sglang/pull/36534) Optimize the heavy memory use of C4 Indexer when BCG is enabled for DSV4
- [#36318](https://github.com/sgl-project/sglang/pull/36318) Add MiniMax-H3 packed varlen path for sla_attn backend
- [#36077](https://github.com/sgl-project/sglang/pull/36077) Fix Qwen3.8 NVFP4 DFlash with Full prefill CUDA graphs
- [#36201](https://github.com/sgl-project/sglang/pull/36201) Bound the EAGLE tree ancestor walk and stop when the ancestor is missing
- [#36278](https://github.com/sgl-project/sglang/pull/36278) Add xpu forward in Gemma3RMSNorm
- [#36153](https://github.com/sgl-project/sglang/pull/36153) Add packed QKV kernel and enable Ulysses SP on CPU
- [#36648](https://github.com/sgl-project/sglang/pull/36648) Route DSA paged top-k through aiter's one-block kernel on ROCm
- [#36504](https://github.com/sgl-project/sglang/pull/36504) Support transposed residual-gate add for diffusion
- [#36655](https://github.com/sgl-project/sglang/pull/36655) Use exact query-head widths for DeepSeek-V4 sparse MLA decode on SM120
- [#36335](https://github.com/sgl-project/sglang/pull/36335) Defer WAR read-done via a dedicated capability for TRTLLM-MHA draft-extend graph replay
- [#36348](https://github.com/sgl-project/sglang/pull/36348) Wave-level optimizations for the legacy top-k transform kernel on ROCm
- [#36488](https://github.com/sgl-project/sglang/pull/36488) Add DSA fused quant+store for per-block fp8 quantize k_nope + bf16 k_rope + paged store

</details>

<details>
<summary>MoE & quantization (38)</summary>

- [#32033](https://github.com/sgl-project/sglang/pull/32033) Support native W4AFP8 checkpoint schemas
- [#31429](https://github.com/sgl-project/sglang/pull/31429) Add FP8 DeepEP dispatch for humming MoE backend
- [#34490](https://github.com/sgl-project/sglang/pull/34490) Add Radix-4 MoE top-k router kernel for Kimi-K3 routing on AMD
- [#30236](https://github.com/sgl-project/sglang/pull/30236) Support INT4 dense linear (AWQ/GPTQ) for XPU
- [#36052](https://github.com/sgl-project/sglang/pull/36052) Load self-describing Quanto INT8 encoders
- [#36036](https://github.com/sgl-project/sglang/pull/36036) Load serialized Comfy W4A8 checkpoints
- [#36023](https://github.com/sgl-project/sglang/pull/36023) Load serialized Comfy ConvRot INT8 native encoders
- [#36046](https://github.com/sgl-project/sglang/pull/36046) Load Comfy NVFP4-AWQ text encoders
- [#35383](https://github.com/sgl-project/sglang/pull/35383) Add the Qwen3.8 MXFP4 MI35x nightly
- [#35180](https://github.com/sgl-project/sglang/pull/35180) Share bounded post-load device staging
- [#36055](https://github.com/sgl-project/sglang/pull/36055) Load MiniMax H3 GGUF text encoders
- [#36039](https://github.com/sgl-project/sglang/pull/36039) Load serialized ConvRot W4A4 checkpoints
- [#34915](https://github.com/sgl-project/sglang/pull/34915) Gather the cutlass MoE activation and its scales in one launch
- [#35994](https://github.com/sgl-project/sglang/pull/35994) Load serialized Comfy ConvRot INT8 DiTs
- [#36543](https://github.com/sgl-project/sglang/pull/36543) Tune LingBot-Video MoE TMA configs for H100
- [#36037](https://github.com/sgl-project/sglang/pull/36037) Support loading mixed w4a8 text encoders
- [#35405](https://github.com/sgl-project/sglang/pull/35405) Fix SM107 MXFP8 activation prep
- [#33323](https://github.com/sgl-project/sglang/pull/33323) Add xpu pass for biased_topk and hash_topk
- [#36044](https://github.com/sgl-project/sglang/pull/36044) Load Comfy NVFP4 MiniMax H3 checkpoints
- [#36275](https://github.com/sgl-project/sglang/pull/36275) Guard FP8 delegate activation params
- [#36061](https://github.com/sgl-project/sglang/pull/36061) Dispatch mixed Comfy NVFP4 and INT8 layers
- [#36237](https://github.com/sgl-project/sglang/pull/36237) Respect padded MXFP8 scale row strides in pre-dispatch
- [#36040](https://github.com/sgl-project/sglang/pull/36040) Support mixed w4a4 and int8 checkpoints
- [#36060](https://github.com/sgl-project/sglang/pull/36060) Infer Comfy FP8 activation scaling
- [#33057](https://github.com/sgl-project/sglang/pull/33057) Enable compressed-tensors FP8 W8A8 on XPU
- [#32039](https://github.com/sgl-project/sglang/pull/32039) Route MoRI through the Qwen MoE all-to-all path on AMD
- [#36122](https://github.com/sgl-project/sglang/pull/36122) Add dense and MoE GGUF MMQ kernels for eight I-quant types
- [#36182](https://github.com/sgl-project/sglang/pull/36182) Migrate gptq_kernel from AOT to JIT
- [#36133](https://github.com/sgl-project/sglang/pull/36133) Fix BF16 physical row semantics and unsupported config checks for MoonEP
- [#36380](https://github.com/sgl-project/sglang/pull/36380) Add Cosmos3 fp8 high precision support
- [#36269](https://github.com/sgl-project/sglang/pull/36269) Add ROCm MegaMoE path via AITER MegaMoEV2
- [#36385](https://github.com/sgl-project/sglang/pull/36385) Enable and fuse the Inkling MoE gate epilogue on Intel XPU
- [#36134](https://github.com/sgl-project/sglang/pull/36134) Support DeepEP expert parallelism on Intel XPU
- [#36559](https://github.com/sgl-project/sglang/pull/36559) Add small-batch sorting path with fused mxfp8 quantisation for MoE
- [#36119](https://github.com/sgl-project/sglang/pull/36119) Optimize MXFP8 MoRI dispatch to match the w4a8 MoE input format
- [#36574](https://github.com/sgl-project/sglang/pull/36574) Add dense-only block convert, torch._scaled_mm 1x32 path, and a bf16 fp8-gemm backend for MXFP8
- [#36137](https://github.com/sgl-project/sglang/pull/36137) Support compressed-tensors quantized lm_head and embed_tokens
- [#36575](https://github.com/sgl-project/sglang/pull/36575) Fuse per-token fp8 quant into add-RMSNorm and fold the MoE all-reduce into the next layer for MiniMax-M3

</details>

<details>
<summary>Model support (18)</summary>

- [#35314](https://github.com/sgl-project/sglang/pull/35314) Support deepseek v4 and kimi k3 on ssd
- [#30360](https://github.com/sgl-project/sglang/pull/30360) Add MiniCPM-SALA support
- [#33561](https://github.com/sgl-project/sglang/pull/33561) Support Ling-3.0-flash (BailingMoeV3)
- [#33569](https://github.com/sgl-project/sglang/pull/33569) Support MiniMax H3 on Ascend NPU's
- [#35963](https://github.com/sgl-project/sglang/pull/35963) Add Spark3 Model
- [#35829](https://github.com/sgl-project/sglang/pull/35829) Support LongCat-Image-Edit and LongCat-Image-Edit-Turbo
- [#36080](https://github.com/sgl-project/sglang/pull/36080) Support hybrid MiniMax H3 conditioning
- [#36076](https://github.com/sgl-project/sglang/pull/36076) Support compact Qwen3-VL conditioning for MiniMax H3
- [#36070](https://github.com/sgl-project/sglang/pull/36070) Load pruned MiniMax H3 components natively
- [#36067](https://github.com/sgl-project/sglang/pull/36067) Load Diffusers MiniMax H3 components natively
- [#36075](https://github.com/sgl-project/sglang/pull/36075) Project MiniMax H3 LoRA onto pruned AdaLN
- [#36606](https://github.com/sgl-project/sglang/pull/36606) Support SenseNova-U1.5-8B-MoT
- [#36311](https://github.com/sgl-project/sglang/pull/36311) Add support for HunyuanImage-3.0-Instruct on NPU
- [#36585](https://github.com/sgl-project/sglang/pull/36585) Add native Qwen4-Exp support
- [#36435](https://github.com/sgl-project/sglang/pull/36435) Add PLaMo3 model support
- [#36567](https://github.com/sgl-project/sglang/pull/36567) Stream PLE embeddings from NVMe for Qwen4
- [#36337](https://github.com/sgl-project/sglang/pull/36337) Add SKT A.X-K2 and ModelOpt NVFP4 support
- [#36332](https://github.com/sgl-project/sglang/pull/36332) Add Qwen3.5 sequence classification support

</details>

<details>
<summary>Parallelism & scheduling (54)</summary>

- [#35791](https://github.com/sgl-project/sglang/pull/35791) Add test-only TreeCore inspector for shared backend tests
- [#34608](https://github.com/sgl-project/sglang/pull/34608) Publish per-scheduler load on a dedicated socket for load-aware routers
- [#27010](https://github.com/sgl-project/sglang/pull/27010) Fix PP inconsistency with HiCache L3
- [#33091](https://github.com/sgl-project/sglang/pull/33091) Stop eviction when shared allocation capacity is sufficient
- [#36232](https://github.com/sgl-project/sglang/pull/36232) Refactor HiCache host pool management
- [#36281](https://github.com/sgl-project/sglang/pull/36281) Add glm5.2 per commit ci for Unified Cache
- [#35927](https://github.com/sgl-project/sglang/pull/35927) Support gated launch to defer startup memory allocation
- [#35640](https://github.com/sgl-project/sglang/pull/35640) Coordinate FullCG prefill across DP-attention ranks
- [#35925](https://github.com/sgl-project/sglang/pull/35925) Make the scheduler track the published weight version
- [#35929](https://github.com/sgl-project/sglang/pull/35929) Report the whole server's world size in the scheduler's internal state
- [#35944](https://github.com/sgl-project/sglang/pull/35944) Pin scheduler metadata before asynchronous H2D copies
- [#34053](https://github.com/sgl-project/sglang/pull/34053) Account resident weight memory in KV sizing
- [#36317](https://github.com/sgl-project/sglang/pull/36317) Keep auxiliary load-back out of Full KV pending ownership
- [#36381](https://github.com/sgl-project/sglang/pull/36381) Fix SWA ownership across grouped frees
- [#36347](https://github.com/sgl-project/sglang/pull/36347) Enable DSV4 DCP HiCache continuation on AMD
- [#36703](https://github.com/sgl-project/sglang/pull/36703) Plan reversible residency before warmup for diffusion
- [#36191](https://github.com/sgl-project/sglang/pull/36191) Add runtime TP/CP switching for MLA on AMD
- [#36409](https://github.com/sgl-project/sglang/pull/36409) Add KVCR as an L3 storage backend for hint-driven cross-instance KV reuse
- [#36720](https://github.com/sgl-project/sglang/pull/36720) Add NVLink collectives, and move the K3 path onto them
- [#36128](https://github.com/sgl-project/sglang/pull/36128) Add C++ unified radix tree backend with FULL+SWA support
- [#36451](https://github.com/sgl-project/sglang/pull/36451) Support PP x PD x DSpark for Kimi K3 and linear drafts
- [#36450](https://github.com/sgl-project/sglang/pull/36450) Support PP x PD x DSpark for DSv4
- [#36147](https://github.com/sgl-project/sglang/pull/36147) Support heterogeneous TP/PP KV cache transfer with Mooncake reshard
- [#36136](https://github.com/sgl-project/sglang/pull/36136) Add dynamic verification for DFlash2
- [#36188](https://github.com/sgl-project/sglang/pull/36188) Add Ascend MemCache storage backend (HiCache L3) and fix L2 cache release issues
- [#36724](https://github.com/sgl-project/sglang/pull/36724) Isolate short multimodal embeddings
- [#36157](https://github.com/sgl-project/sglang/pull/36157) Overlap multimodal preprocessing with ViT execution
- [#36297](https://github.com/sgl-project/sglang/pull/36297) Enable CP-v2 interleave for FlashMLA sparse prefill
- [#36610](https://github.com/sgl-project/sglang/pull/36610) Add deferred decode-side KV release on the zmq-mitigation base for Kimi-K3
- [#36310](https://github.com/sgl-project/sglang/pull/36310) Add cache-hit-aware over-admission for bounded Mamba requests
- [#36261](https://github.com/sgl-project/sglang/pull/36261) Support pipeline parallelism for dflash2 speculative decoding
- [#36489](https://github.com/sgl-project/sglang/pull/36489) Prevent rank divergence in multimodal input broadcast
- [#36631](https://github.com/sgl-project/sglang/pull/36631) Support sampling masks with overlap scheduling
- [#36471](https://github.com/sgl-project/sglang/pull/36471) Add SeaCache algorithm for diffusion acceleration
- [#36516](https://github.com/sgl-project/sglang/pull/36516) Support block verification for rejection sampling
- [#36651](https://github.com/sgl-project/sglang/pull/36651) Add PD state transfer for Flash Next
- [#36449](https://github.com/sgl-project/sglang/pull/36449) Support PP x PD transfer for DSv4
- [#36612](https://github.com/sgl-project/sglang/pull/36612) Share the prefill->decode failure notification across backends
- [#36661](https://github.com/sgl-project/sglang/pull/36661) Tie overlap batch snapshot lifetime to result completion
- [#36700](https://github.com/sgl-project/sglang/pull/36700) Add PP Prefetch Tickets for eager cross-stage storage prefetch
- [#36185](https://github.com/sgl-project/sglang/pull/36185) Make DSV4 retraction safe
- [#36613](https://github.com/sgl-project/sglang/pull/36613) Add PP PD admission flow
- [#36345](https://github.com/sgl-project/sglang/pull/36345) Support Mamba in buffer-only host memory mode
- [#36112](https://github.com/sgl-project/sglang/pull/36112) Prototype Qwen3-Next native MTP path
- [#36248](https://github.com/sgl-project/sglang/pull/36248) Support prefill CUDA graph proxy tensors
- [#36721](https://github.com/sgl-project/sglang/pull/36721) Add `free_kv_row` to release a request's kv row by row range
- [#36026](https://github.com/sgl-project/sglang/pull/36026) Support diffusion decoder parallel tiling for LTX-2.5
- [#36707](https://github.com/sgl-project/sglang/pull/36707) Prevent abort ACK with unresolved errored transfers
- [#36288](https://github.com/sgl-project/sglang/pull/36288) Add Mixed Chunk Prefill Base
- [#36109](https://github.com/sgl-project/sglang/pull/36109) Use model-native video preprocessing for Qwen3-VL
- [#36350](https://github.com/sgl-project/sglang/pull/36350) Preserve restored SWA lock ownership
- [#36540](https://github.com/sgl-project/sglang/pull/36540) Avoid sampling-mask synchronization in decode
- [#36227](https://github.com/sgl-project/sglang/pull/36227) Retry L3 storage prefetch after a missed attempt
- [#36244](https://github.com/sgl-project/sglang/pull/36244) Shard QKV weights across TP and Ulysses for MiniMax-H3
- [#36341](https://github.com/sgl-project/sglang/pull/36341) Add KL guards for HiCache buffer-only host memory mode
- [#36637](https://github.com/sgl-project/sglang/pull/36637) Add `free_full` to release the full side of a tombstoned SWA node
- [#36370](https://github.com/sgl-project/sglang/pull/36370) Batch radix eviction frees into one drain per KV component
- [#36049](https://github.com/sgl-project/sglang/pull/36049) Clean up stale staging watermark subscribers

</details>

<details>
<summary>Hardware & arch (13)</summary>

- [#35072](https://github.com/sgl-project/sglang/pull/35072) Support prefill only models for xpu
- [#33354](https://github.com/sgl-project/sglang/pull/33354) Use a fused GDN kernel from sgl-kernel for Qwen3.5 on XPU
- [#34492](https://github.com/sgl-project/sglang/pull/34492) Remove SGLANG_USE_SGL_XPU flag
- [#32166](https://github.com/sgl-project/sglang/pull/32166) Use SYCL kernels for DeepSeek V4 MHC on XPU
- [#29143](https://github.com/sgl-project/sglang/pull/29143) Add intel_xpu to DETERMINISTIC_ATTENTION_BACKEND_CHOICES
- [#36164](https://github.com/sgl-project/sglang/pull/36164) Serve Apple Silicon decode through one exported whole-model MLX region
- [#36581](https://github.com/sgl-project/sglang/pull/36581) Enable DeepSeek-V4 FP4 Indexer on ROCm gfx950
- [#36490](https://github.com/sgl-project/sglang/pull/36490) Add gfx1250 ROCm 10.0 RC4 release image
- [#36607](https://github.com/sgl-project/sglang/pull/36607) Enable GLM-5.3-Flash on gfx942 and gfx950
- [#36710](https://github.com/sgl-project/sglang/pull/36710) Serve Apple Silicon through the standard Torch ModelRunner and retire the standalone MLX runner routing
- [#36144](https://github.com/sgl-project/sglang/pull/36144) Enable --cuda-graph-backend-prefill=tc_piecewise on MI355X
- [#36434](https://github.com/sgl-project/sglang/pull/36434) Add ROCm 10.0.0 GA (gfx942 / gfx950) validation
- [#36472](https://github.com/sgl-project/sglang/pull/36472) Add base NpuSRTPlatform implementation

</details>

<details>
<summary>API & serving (17)</summary>

- [#35926](https://github.com/sgl-project/sglang/pull/35926) Report per-token weight-version spans in generation meta info
- [#30918](https://github.com/sgl-project/sglang/pull/30918) Add optional steady-state window for serving metrics
- [#35349](https://github.com/sgl-project/sglang/pull/35349) Size the multimodal preprocessing pool by where preprocessing runs
- [#36084](https://github.com/sgl-project/sglang/pull/36084) Add per-component quantization overrides
- [#36034](https://github.com/sgl-project/sglang/pull/36034) Clean up startup and offload logs
- [#35342](https://github.com/sgl-project/sglang/pull/35342) Route every multimodal processor through the worker pool's call site
- [#36078](https://github.com/sgl-project/sglang/pull/36078) Add composable component weight path CLI
- [#36085](https://github.com/sgl-project/sglang/pull/36085) Support VAE weight-file overrides
- [#36086](https://github.com/sgl-project/sglang/pull/36086) Add plain component weight overrides
- [#36313](https://github.com/sgl-project/sglang/pull/36313) Add --speculative-dsa-topk-backend
- [#36718](https://github.com/sgl-project/sglang/pull/36718) Decouple preprocessing from rust server
- [#36069](https://github.com/sgl-project/sglang/pull/36069) Add InferCast time predictor adapter
- [#36319](https://github.com/sgl-project/sglang/pull/36319) Support out-of-tree platforms and hook plugins for diffusion
- [#36272](https://github.com/sgl-project/sglang/pull/36272) Keep buffered decode steps observable so tool-call runs report real ITL/TPOT
- [#36141](https://github.com/sgl-project/sglang/pull/36141) Add /v1/responses support to the HTTP PD router
- [#36630](https://github.com/sgl-project/sglang/pull/36630) Capture masks from sampler support
- [#36213](https://github.com/sgl-project/sglang/pull/36213) Support temperature-scaled input logprobs

</details>

<details>
<summary>Tests, CI & build (33)</summary>

- [#35227](https://github.com/sgl-project/sglang/pull/35227) Register CPU CI for 17 e2e tests and partition xeon base-c suite
- [#36100](https://github.com/sgl-project/sglang/pull/36100) Trigger pr-test-xpu on multimodal_gen changes
- [#35686](https://github.com/sgl-project/sglang/pull/35686) Name the ROCm Image That Actually Ran in AMD Job Names
- [#36284](https://github.com/sgl-project/sglang/pull/36284) Add Kimi-K3 MMMU-Pro accuracy coverage
- [#36396](https://github.com/sgl-project/sglang/pull/36396) Add DeepSeek-V4-Flash FP8 accuracy coverage on MI30x
- [#36241](https://github.com/sgl-project/sglang/pull/36241) Cut repeated tokenizer loads, serial subprocesses and a double scan
- [#36142](https://github.com/sgl-project/sglang/pull/36142) Add MiniMax-M3-MXFP8 MI35x nightly perf benchmark
- [#36240](https://github.com/sgl-project/sglang/pull/36240) Stop the config ratchets re-parsing the package on every scan
- [#36051](https://github.com/sgl-project/sglang/pull/36051) Guard the anonymous-host budget alongside peak VRAM
- [#36180](https://github.com/sgl-project/sglang/pull/36180) Combine NPU test fixes from #35472 and #34516
- [#36413](https://github.com/sgl-project/sglang/pull/36413) Fix a few issues that cause XEON CI failures
- [#36636](https://github.com/sgl-project/sglang/pull/36636) Add targeted Mori test labels
- [#36605](https://github.com/sgl-project/sglang/pull/36605) Graceful teardown for the radix_cache server fixtures
- [#34057](https://github.com/sgl-project/sglang/pull/34057) Rerun cancelled runs and target the newest run per workflow
- [#36171](https://github.com/sgl-project/sglang/pull/36171) Temporarily bypass local-registry image pulls
- [#36393](https://github.com/sgl-project/sglang/pull/36393) Restore MiniMax-M2.5 4-GPU MI35x nightly job
- [#36296](https://github.com/sgl-project/sglang/pull/36296) Fix shared-KV verify tests for multi-head GQA
- [#36126](https://github.com/sgl-project/sglang/pull/36126) Add unit tests for hardware_backend/npu/modules
- [#36125](https://github.com/sgl-project/sglang/pull/36125) Add unit tests for graph_runner module
- [#36117](https://github.com/sgl-project/sglang/pull/36117) Update CI test est_time values
- [#36642](https://github.com/sgl-project/sglang/pull/36642) Run Kimi-K3 gpqa in nightly with source build
- [#36282](https://github.com/sgl-project/sglang/pull/36282) Fix NPU e2e framework hang and add single-case repeat/stress workflow
- [#36355](https://github.com/sgl-project/sglang/pull/36355) Add DSV4-Flash DSPARK / GLM-5.2 / Kimi-K3 gpqa accuracy cases, register to nightly
- [#36682](https://github.com/sgl-project/sglang/pull/36682) Run GLM-5.2 gpqa in nightly
- [#36484](https://github.com/sgl-project/sglang/pull/36484) Fix NPU test-case timeout and narrow nightly workflow
- [#36667](https://github.com/sgl-project/sglang/pull/36667) Make qwen4-main-squashed pre-commit clean
- [#36073](https://github.com/sgl-project/sglang/pull/36073) Add PD combo scenario unit tests
- [#36114](https://github.com/sgl-project/sglang/pull/36114) Add a model cache audit that counts per-commit workflows
- [#36539](https://github.com/sgl-project/sglang/pull/36539) Add glm53 router image
- [#36106](https://github.com/sgl-project/sglang/pull/36106) Add unit tests for Triton load watch
- [#36709](https://github.com/sgl-project/sglang/pull/36709) Add MUSA installation guide and Dockerfile
- [#36236](https://github.com/sgl-project/sglang/pull/36236) Add DeepSeek-R1-0528 FP8 HiCache 1P1D nightly recipe
- [#36441](https://github.com/sgl-project/sglang/pull/36441) Add unit tests for scheduler IPC channels
- [#36378](https://github.com/sgl-project/sglang/pull/36378) Resolve the nightly image tag with git ls-remote instead of fetching tags
- plus 18 more config resolution and parsing updates

</details>

<details>
<summary>Docs (33)</summary>

- [#36016](https://github.com/sgl-project/sglang/pull/36016) Refresh quality and BCG benchmark skills
- [#36301](https://github.com/sgl-project/sglang/pull/36301) Support batching for cosmos3 action generation
- [#36496](https://github.com/sgl-project/sglang/pull/36496) Add Qwen3.8-Flash-Next cookbook
- [#36440](https://github.com/sgl-project/sglang/pull/36440) Add GLM-5.3-Flash cookbook
- [#36286](https://github.com/sgl-project/sglang/pull/36286) Add IBM Granite 4.2 cookbook
- [#36028](https://github.com/sgl-project/sglang/pull/36028) Add MiniMax H3 checkpoint format table
- [#35508](https://github.com/sgl-project/sglang/pull/35508) Add Ascend NPU (A3) recipe to the Kimi-K3 cookbook
- [#36463](https://github.com/sgl-project/sglang/pull/36463) Make benchmark caches seedable and cover missing native families
- [#36020](https://github.com/sgl-project/sglang/pull/36020) Split the Qwen3.8-27B NVFP4 cells by lm_head precision
- [#36246](https://github.com/sgl-project/sglang/pull/36246) Add Kimi-K2.7-Code-MXFP4 to cookbook
- [#35836](https://github.com/sgl-project/sglang/pull/35836) Refresh supported features and models on Ascend NPU
- [#36544](https://github.com/sgl-project/sglang/pull/36544) GLM-5.3-Flash cookbook: HiCache for LL, fusion-flag drop, EAGLE, default-cell numbers, DCP4 overlay
- [#36519](https://github.com/sgl-project/sglang/pull/36519) GLM-5.3-Flash cookbook: default Blackwell recipes to FP8 KV + TRT-LLM DSA
- [#36608](https://github.com/sgl-project/sglang/pull/36608) Add GLM-5.3-Flash recipes for MI300X, MI325X, and MI355X
- [#36660](https://github.com/sgl-project/sglang/pull/36660) Fix GLM-5.3-Flash speculative flag, size Hopper memory, record GSM8K
- [#35961](https://github.com/sgl-project/sglang/pull/35961) Reuse SANA fast paths in SANA-Video BCG
- [#36485](https://github.com/sgl-project/sglang/pull/36485) Align video BCG warmup frame count
- [#36325](https://github.com/sgl-project/sglang/pull/36325) Update CANN version in NPU installation docs
- [#36513](https://github.com/sgl-project/sglang/pull/36513) GLM-5.3-Flash cookbook: FP8 KV + TRT-LLM benchmark cards and Blackwell default
- [#36000](https://github.com/sgl-project/sglang/pull/36000) Keep Cosmos3 Nano resident on high-memory GPUs
- [#36169](https://github.com/sgl-project/sglang/pull/36169) Add desktop-safe 24 GB recipe and the DGX Spark tier
- [#36008](https://github.com/sgl-project/sglang/pull/36008) Reject unsafe quality=high BCG replay
- [#35416](https://github.com/sgl-project/sglang/pull/35416) Sync LMSYS SGLang blog cards
- [#36204](https://github.com/sgl-project/sglang/pull/36204) Mark Ling-3.0-flash DSPARK verified for all four quantizations on H200
- [#36364](https://github.com/sgl-project/sglang/pull/36364) Add GB10 (DGX Spark) MXFP4 cells for Ling-3.0-flash
- [#36553](https://github.com/sgl-project/sglang/pull/36553) Accept mesh benchmark artifacts
- [#35993](https://github.com/sgl-project/sglang/pull/35993) Keep LongLive2 components resident on large GPUs
- [#35854](https://github.com/sgl-project/sglang/pull/35854) Update amd deepseek v4 cookbook 0822
- [#36476](https://github.com/sgl-project/sglang/pull/36476) Update npu best practice
- [#36091](https://github.com/sgl-project/sglang/pull/36091) Add NPU profiler analysis skill
- [#36089](https://github.com/sgl-project/sglang/pull/36089) Consolidated NPU graph mode usage guide
- [#36116](https://github.com/sgl-project/sglang/pull/36116) Fix multi-node example, add single-node and offline batch examples
- [#36712](https://github.com/sgl-project/sglang/pull/36712) Add GLM-5.3-Flash MXFP4 recipes for MI350X and MI355X

</details>

<details>
<summary>Bugfixes (37)</summary>

- [#34237](https://github.com/sgl-project/sglang/pull/34237) Recover tool calls dropped by common model-output
- [#36239](https://github.com/sgl-project/sglang/pull/36239) Fix glm a5 cache
- [#34668](https://github.com/sgl-project/sglang/pull/34668) Stabilize nightly precision regression
- [#33859](https://github.com/sgl-project/sglang/pull/33859) Crop GLM-Image output to requested size
- [#36595](https://github.com/sgl-project/sglang/pull/36595) Re-encode multimodal embeddings after cache mismatch
- [#36029](https://github.com/sgl-project/sglang/pull/36029) Refresh stale prefill bootstrap metadata
- [#36097](https://github.com/sgl-project/sglang/pull/36097) Fix MXFP8 MoE weight sizing for non-gated models
- [#36295](https://github.com/sgl-project/sglang/pull/36295) Bound CUDA memory for fast image preprocessing
- [#35957](https://github.com/sgl-project/sglang/pull/35957) Fix recurrent state loss on decode retraction
- [#35275](https://github.com/sgl-project/sglang/pull/35275) Fix startup crash and reduce CUDA graph memory usage for speculative adaptive
- [#35646](https://github.com/sgl-project/sglang/pull/35646) Detect cross-node multimodal transport by nnodes
- [#32856](https://github.com/sgl-project/sglang/pull/32856) Fix NUMA/core binding for DP ranks
- [#36398](https://github.com/sgl-project/sglang/pull/36398) Fix MiniMax-H3 dp_size>1 deadlock and cross-request audio determinism
- [#35832](https://github.com/sgl-project/sglang/pull/35832) Fix a refit KeyError on mapped weights, and stop claiming strides the reload discards
- [#36542](https://github.com/sgl-project/sglang/pull/36542) Fix native LingBot-Video text encoding
- [#34715](https://github.com/sgl-project/sglang/pull/34715) Fix transpose batch matmul K*B exceed 65536 on NPU
- [#36190](https://github.com/sgl-project/sglang/pull/36190) Verify distributed adapter checksums
- [#36420](https://github.com/sgl-project/sglang/pull/36420) Fix HiCache storage keys to include kv_cache_dtype
- [#36626](https://github.com/sgl-project/sglang/pull/36626) Resolve tool argument types through top-level anyOf/oneOf/allOf
- [#36339](https://github.com/sgl-project/sglang/pull/36339) Fix DeepSeekV32Detector streaming corrupting tool-call arguments
- [#36688](https://github.com/sgl-project/sglang/pull/36688) Fix GLM detectors: streamed tool-call arguments disagree with non-streaming
- [#36695](https://github.com/sgl-project/sglang/pull/36695) Fix step3: parameterless tool calls are dropped, batched calls get mixed up
- [#36659](https://github.com/sgl-project/sglang/pull/36659) Fix EAGLE3 TARGET_VERIFY on MI300 + AITER unquant MoE
- [#36643](https://github.com/sgl-project/sglang/pull/36643) Fix memory-saver subprocess crash on CUDA 13 pip envs
- [#36418](https://github.com/sgl-project/sglang/pull/36418) Fix zombie requests after streaming disconnect
- [#36713](https://github.com/sgl-project/sglang/pull/36713) Evict Full KV for Mamba byte shortfalls
- [#36158](https://github.com/sgl-project/sglang/pull/36158) Ask the checkpoint whether mtp.* is quantized for Qwen3.5 MTP
- [#36173](https://github.com/sgl-project/sglang/pull/36173) Make top-k/top-p filtering consistent across sampling paths
- [#36552](https://github.com/sgl-project/sglang/pull/36552) Abort streaming-session requests on client disconnect
- [#36108](https://github.com/sgl-project/sglang/pull/36108) Notify decode of NIXL transfer failures
- [#36331](https://github.com/sgl-project/sglang/pull/36331) Fix layer indexing and enable prefetch under PP
- [#36320](https://github.com/sgl-project/sglang/pull/36320) Fix MiniMax H3 WebUI inference settings
- [#36524](https://github.com/sgl-project/sglang/pull/36524) Bound NIXL hybrid bounce transfers
- [#36696](https://github.com/sgl-project/sglang/pull/36696) Register a split node under its own key in the mamba radix cache
- [#36354](https://github.com/sgl-project/sglang/pull/36354) Omit DSV4/DSV32 tools when tool_choice=none
- [#36691](https://github.com/sgl-project/sglang/pull/36691) Fix minimax-m2: streaming tool calls are lost and markers leak into content
- [#36483](https://github.com/sgl-project/sglang/pull/36483) Support root JSON Schema combinators in tool parsers

</details>

<details>
<summary>Refactors (9)</summary>

- [#36222](https://github.com/sgl-project/sglang/pull/36222) Migrate tests to strategy-based prefill CP
- [#36586](https://github.com/sgl-project/sglang/pull/36586) Refactor server argument choices
- [#36676](https://github.com/sgl-project/sglang/pull/36676) Refactor server_args constants and layout
- [#36416](https://github.com/sgl-project/sglang/pull/36416) Rename Spark3 to Spark2.5
- [#36031](https://github.com/sgl-project/sglang/pull/36031) Dedupe mooncake failure_exception into a mixin
- [#36228](https://github.com/sgl-project/sglang/pull/36228) Remove generic prefill CP v1 runtime
- [#36229](https://github.com/sgl-project/sglang/pull/36229) Canonicalize prefill CP API names
- [#36223](https://github.com/sgl-project/sglang/pull/36223) Make strategy prefill CP canonical
- [#36072](https://github.com/sgl-project/sglang/pull/36072) Centralize stream management for NPU

</details>

<details>
<summary>Other (40)</summary>

- [#33684](https://github.com/sgl-project/sglang/pull/33684) Support static DP/EP layouts
- [#36062](https://github.com/sgl-project/sglang/pull/36062) Cache LoRA-merged weights in files the page cache can hold
- [#36160](https://github.com/sgl-project/sglang/pull/36160) Align prefill transfer control plane for unified control plane
- [#35343](https://github.com/sgl-project/sglang/pull/35343) Sync FlashInfer autotune tactic choice across TP ranks
- [#35986](https://github.com/sgl-project/sglang/pull/35986) Re-home decode-dtype VAE weights to a file-backed store
- [#36300](https://github.com/sgl-project/sglang/pull/36300) Key the model-config cache on the path the record carried
- [#35840](https://github.com/sgl-project/sglang/pull/35840) Add PD test for inkling with mxfp8 KV
- [#35734](https://github.com/sgl-project/sglang/pull/35734) Park a layerwise component's non-layer weights between uses
- [#36082](https://github.com/sgl-project/sglang/pull/36082) Infer LoRA alpha from safetensors metadata
- [#36708](https://github.com/sgl-project/sglang/pull/36708) Support GLM-5.3-Flash hidden-state capture
- [#36198](https://github.com/sgl-project/sglang/pull/36198) Enhance test and support EPLB
- [#36024](https://github.com/sgl-project/sglang/pull/36024) Speed up LingBot high-quality VAE decode
- [#33634](https://github.com/sgl-project/sglang/pull/33634) Add test for --dllm-fdfo
- [#36053](https://github.com/sgl-project/sglang/pull/36053) Move cuda_vmm_utils.py under srt/utils/
- [#36025](https://github.com/sgl-project/sglang/pull/36025) Deduplicate CP-replicated state transfers
- [#35506](https://github.com/sgl-project/sglang/pull/35506) Add graph register for fused_sigmoid_mul_cpu, fused_qk_gemma_rmsnorm
- [#35379](https://github.com/sgl-project/sglang/pull/35379) Generalize hybrid SWA MTP draft pool routing
- [#36299](https://github.com/sgl-project/sglang/pull/36299) Make daemon socket/ready paths configurable via env
- [#36384](https://github.com/sgl-project/sglang/pull/36384) Streamed LoRA weight updates: register RPC, session scope, LoRA stash
- [#36279](https://github.com/sgl-project/sglang/pull/36279) Support daemon-to-daemon heterogeneous weight resharding with Mooncake backend
- [#36196](https://github.com/sgl-project/sglang/pull/36196) Add Dflash2 tree drafting
- [#36293](https://github.com/sgl-project/sglang/pull/36293) Add Daemon To Daemon transfer backend
- [#36670](https://github.com/sgl-project/sglang/pull/36670) Pcp rebase bak
- [#36156](https://github.com/sgl-project/sglang/pull/36156) Add disk-vs-daemon parity harness; fix persistence, zombie-PID liveness, and SM100 block-FP8 gating
- [#36045](https://github.com/sgl-project/sglang/pull/36045) Make FlashInfer NVFP4 speculative decoding graph-safe
- [#36389](https://github.com/sgl-project/sglang/pull/36389) Support DP attention in LoRA backends
- [#36192](https://github.com/sgl-project/sglang/pull/36192) In-place LoRA merge/unmerge under layerwise offload
- [#36403](https://github.com/sgl-project/sglang/pull/36403) Support speculative decoding with unified SWA memory
- [#36101](https://github.com/sgl-project/sglang/pull/36101) Key daemon paths by GPU UUID
- [#36096](https://github.com/sgl-project/sglang/pull/36096) Keep Qwen3.6 hybrid SSM state stable across radix modes
- [#36474](https://github.com/sgl-project/sglang/pull/36474) Enhance Hicache observability and logging capabilities
- [#36372](https://github.com/sgl-project/sglang/pull/36372) Sync-free in-place out-of-window SWA frees
- [#36163](https://github.com/sgl-project/sglang/pull/36163) Avoid redundant CPU embedding materialization in the unpooled ZMQ path
- [#36074](https://github.com/sgl-project/sglang/pull/36074) Add llguidance bitmask path for Ascend NPU
- [#36323](https://github.com/sgl-project/sglang/pull/36323) Advise the kernel ahead of the courier on mapped layers
- [#35850](https://github.com/sgl-project/sglang/pull/35850) Restrict MiniMax-H3 SubBlock sparsity to video queries
- [#35915](https://github.com/sgl-project/sglang/pull/35915) Drop empty assistant turns for mistral_common tokenizers
- [#36249](https://github.com/sgl-project/sglang/pull/36249) Support out-of-tree torch.compile backends
- [#35505](https://github.com/sgl-project/sglang/pull/35505) Enable shared-experts fusion on the flashinfer_mxfp4 (trtllm-gen) MoE path
- [#27723](https://github.com/sgl-project/sglang/pull/27723) Add RDT/NIXL weight sync support for Ray scheduler actors

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (sglang.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 598dc6dc28130c6897b797a263fa04f9d22dc5bc6d59dd302fe984b05f02655d -->
