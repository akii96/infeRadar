# vllm: PR digest (2026-06-24 to 2026-06-28)

_194 merged, 222 newly opened - source vllm-project/vllm, generated 2026-06-28T22:13:37Z_

## TL;DR
- DeepSeek (V3.2/V4) and GLM5 dominated the cycle, with merged op fusions and router GEMMs for GLM5/DSV3.2, plus in-flight work on DeepSeek V4 sequence parallelism and DSpark speculative decoding.
- Major KV cache quantization breakthroughs are in progress, including newly opened PRs for KVarN (calibration-free variance-normalized) and Oscar-2 (2-bit KV cache), alongside a merged Triton INT4 per-token-head KV cache implementation.
- The Rust frontend saw massive churn, introducing a unified parser interface, streaming parser engine, and strict structural-tag tool calling integration.
- Significant MoE performance wins landed, including fused shared expert (FSE) support for GLM-4.5/6/7 and MiniMax-M3 on ROCm, plus NVFP4 weight dequantization fused with compute in Triton.

## Most important PRs
- **[#46812](https://github.com/vllm-project/vllm/pull/46812)**: Introduces KVarN, a novel calibration-free variance-normalized KV-cache quantization backend that significantly reduces memory footprint while maintaining accuracy.
- **[#40835](https://github.com/vllm-project/vllm/pull/40835)**: Implements INT4 KV cache quantization at a per-token-head granularity using Triton, unlocking higher batch sizes and longer contexts for memory-bound deployments.
- **[#46876](https://github.com/vllm-project/vllm/pull/46876)**: Fuses attention and kernel operations specifically for GLM5 and DeepSeek V3.2 on NVIDIA hardware, directly improving end-to-end throughput for these heavily-used models.
- **[#46583](https://github.com/vllm-project/vllm/pull/46583)**: A massive architectural refactor of the Rust frontend that unifies parsing logic, paving the way for more robust and performant streaming and tool-calling capabilities.
- **[#44667](https://github.com/vllm-project/vllm/pull/44667)**: Optimizes MoE execution by fusing NVFP4 dequantization directly into the MLP compute kernels, reducing memory bandwidth pressure during expert routing.

## More changes by area

<details>
<summary>Performance (24)</summary>

- [#46546](https://github.com/vllm-project/vllm/pull/46546) Optimize sparse attention on minimax-m3 on ROCm
- [#46353](https://github.com/vllm-project/vllm/pull/46353) Accelerate unquantized MoE for AArch64 CPUs
- [#46184](https://github.com/vllm-project/vllm/pull/46184) Use flydsl MoE with Minimax-M3 mxfp8 weights on gfx950
- [#44313](https://github.com/vllm-project/vllm/pull/44313) Add Fused Shared Expert (FSE) support for GLM-4.5/6/7 on ROCm
- [#45033](https://github.com/vllm-project/vllm/pull/45033) Add AITER FlashAttention MLA prefill backend for ROCm
- [#46862](https://github.com/vllm-project/vllm/pull/46862) Improve GLM5.2 throughput via fused_indexer_q_rope_quant Triton kernel
- [#46545](https://github.com/vllm-project/vllm/pull/46545) Enable shared-expert fusion for bias-routed MoE on MiniMax-M3
- [#46635](https://github.com/vllm-project/vllm/pull/46635) Replace MOE all-reduce with reduce-scatter for GLM5.2
- [#45971](https://github.com/vllm-project/vllm/pull/45971) Parallelize KV load with a receive-thread pool for Mooncake
- [#40784](https://github.com/vllm-project/vllm/pull/40784) Tune wvSplitK on gfx1151 for ROCm
- [#46425](https://github.com/vllm-project/vllm/pull/46425) Reduce search space for thinking tokens
- [#46474](https://github.com/vllm-project/vllm/pull/46474) Add fused shared expert for Minimax M3 on ROCm
- [#46122](https://github.com/vllm-project/vllm/pull/46122) Optimize AITER MoE for DeepSeekV4 on ROCm
- [#46392](https://github.com/vllm-project/vllm/pull/46392) Enable and tune FlashInfer fused allreduce at world_size=16 on SM 10.3
- [#46542](https://github.com/vllm-project/vllm/pull/46542) Replace O(n) list.index() with a dict in LoRA convert_mapping
- [#46651](https://github.com/vllm-project/vllm/pull/46651) Remove redundant clone for GLM and DeepSeek models
- [#46543](https://github.com/vllm-project/vllm/pull/46543) Avoid building a full timestamps list in video frame sampling
- [#46703](https://github.com/vllm-project/vllm/pull/46703) Extend NCCL symmetric memory to AllGather and ReduceScatter (opened)
- [#46750](https://github.com/vllm-project/vllm/pull/46750) Expand Triton kernel warmup coverage for Qwen (opened)
- [#46634](https://github.com/vllm-project/vllm/pull/46634) Expand Triton kernel warmup coverage for DSv4 (opened)
- [#46911](https://github.com/vllm-project/vllm/pull/46911) Fuse DFlash cache insert kernel (opened)
- [#46832](https://github.com/vllm-project/vllm/pull/46832) Cap sparse MLA decode KV-splits with a work-per-split heuristic on ROCm (opened)
- [#46935](https://github.com/vllm-project/vllm/pull/46935) AsyncTP fusion for dynamic per-group FP8 scaled_mm + comms (opened)
- [#46716](https://github.com/vllm-project/vllm/pull/46716) Fix shared-memory all-reduce deadlock across nodes on CPU (opened)
</details>

<details>
<summary>Kernels & attention (40)</summary>

- [#44044](https://github.com/vllm-project/vllm/pull/44044) Support DCP with FP8 KV cache in MLA decode path
- [#46189](https://github.com/vllm-project/vllm/pull/46189) Add FLASH_ATTN_MLA_SPARSE backend for Hopper sparse MLA
- [#44029](https://github.com/vllm-project/vllm/pull/44029) Enable DFlash speculative decoding for CPU
- [#46405](https://github.com/vllm-project/vllm/pull/46405) Remove dead kernel code
- [#46643](https://github.com/vllm-project/vllm/pull/46643) Vectorize fp32 moe_sum reduction and support any topk
- [#46385](https://github.com/vllm-project/vllm/pull/46385) Add GLM5 Router GEMM kernel
- [#46761](https://github.com/vllm-project/vllm/pull/46761) Fuse precompute kv per-layer rmsnorms for DFlash
- [#46508](https://github.com/vllm-project/vllm/pull/46508) Enable PDL for per_token_group_quant_8bit_kernel
- [#46409](https://github.com/vllm-project/vllm/pull/46409) Fix test_concat_and_cache_mla_rope_fused on ROCm
- [#46780](https://github.com/vllm-project/vllm/pull/46780) Fix AITER_UNIFIED_ATTN dispatching after AITER bump
- [#46550](https://github.com/vllm-project/vllm/pull/46550) Fix topk histogram build on SM75
- [#46548](https://github.com/vllm-project/vllm/pull/46548) Fix OOB during model warmup with ROCM_ATTN and MRV2
- [#46691](https://github.com/vllm-project/vllm/pull/46691) Use Triton-based AITER MHA for LM Eval Qwen-3.5 tests
- [#46753](https://github.com/vllm-project/vllm/pull/46753) Fix cross-attention block table sizing
- [#46555](https://github.com/vllm-project/vllm/pull/46555) Set AttentionCGSupport.UNIFORM_BATCH for FA2 on XPU
- [#46644](https://github.com/vllm-project/vllm/pull/46644) Update vllm to point to flash-attention commit building FA3 with torch stable API
- [#46961](https://github.com/vllm-project/vllm/pull/46961) Fix minor typo in GLM5
- [#46903](https://github.com/vllm-project/vllm/pull/46903) Add Oscar KV cache support (opened)
- [#46570](https://github.com/vllm-project/vllm/pull/46570) Add MRV2 virtual-batch PCP for MLA (opened)
- [#46912](https://github.com/vllm-project/vllm/pull/46912) Pre-copy-free align prefix cache for model runner V1 and V2 (opened)
- [#46774](https://github.com/vllm-project/vllm/pull/46774) Add Oscar-2 2-bit KV cache quantisation backend (opened)
- [#46963](https://github.com/vllm-project/vllm/pull/46963) Use FlashInfer for pre-SM100 NVFP4 KV cache updates (opened)
- [#46883](https://github.com/vllm-project/vllm/pull/46883) Use FlashInfer workspace sizing helper (opened)
- [#46896](https://github.com/vllm-project/vllm/pull/46896) Enable GDN all-mode Mamba prefix caching with Mooncake Store retention (opened)
- [#46592](https://github.com/vllm-project/vllm/pull/46592) Add invariant with prefix cache (opened)
- [#46742](https://github.com/vllm-project/vllm/pull/46742) Integrate TokenSpeed MHA for GPTOSS on ROCm (opened)
- [#46558](https://github.com/vllm-project/vllm/pull/46558) Enable FlashInfer mm-prefix attention (opened)
- [#46849](https://github.com/vllm-project/vllm/pull/46849) Fuse AR speculator multi-step decodes back into one CUDA graph (opened)
- [#46724](https://github.com/vllm-project/vllm/pull/46724) Add occupancy-gated 3D segmented decode for multi-query over long KV (opened)
- [#46819](https://github.com/vllm-project/vllm/pull/46819) Add Triton MLA logits workspace (opened)
- [#46908](https://github.com/vllm-project/vllm/pull/46908) Handle list slot mappings in attention context (opened)
- [#46597](https://github.com/vllm-project/vllm/pull/46597) Prefer ROCM_AITER_FA over ROCM_ATTN when AITER MHA is enabled (opened)
- [#46952](https://github.com/vllm-project/vllm/pull/46952) Pad FP8 MLA decode head count to a native value on gfx950 (opened)
- [#46763](https://github.com/vllm-project/vllm/pull/46763) Fix ROCm sparse MLA long context seq len guard (opened)
- [#46754](https://github.com/vllm-project/vllm/pull/46754) Defer to TRITON_ATTN backend for Prefix LM models on ROCm (opened)
- [#46847](https://github.com/vllm-project/vllm/pull/46847) Window-correct shuffled fp8 decode for SWA layers on ROCm (opened)
- [#46842](https://github.com/vllm-project/vllm/pull/46842) Remove dead minimax allreduce rms kernel (opened)
- [#46640](https://github.com/vllm-project/vllm/pull/46640) Test FA2 remove dropout (opened)
- [#46659](https://github.com/vllm-project/vllm/pull/46659) Fix FA4 dynamic_causal for full attention layers (opened)
- [#46943](https://github.com/vllm-project/vllm/pull/46943) Update FlashInfer compute support to 7.5 (opened)
- [#46638](https://github.com/vllm-project/vllm/pull/46638) Add FlashInfer CuteDSL non-causal decode path for DFlash (opened)
</details>

<details>
<summary>MoE & quantization (45)</summary>

- [#46706](https://github.com/vllm-project/vllm/pull/46706) Remove grok model arch from vllm
- [#45924](https://github.com/vllm-project/vllm/pull/45924) Add HPC-Ops MoE backend
- [#43461](https://github.com/vllm-project/vllm/pull/43461) Add MoE kernel oracle abc 37753
- [#46820](https://github.com/vllm-project/vllm/pull/46820) Fix Transformers backend FP8 MoE and remove boilerplate
- [#46642](https://github.com/vllm-project/vllm/pull/46642) Tune block-FP8 fused MoE for low-batch decode
- [#46758](https://github.com/vllm-project/vllm/pull/46758) Refactor and fix deepep_moe test group on ROCm
- [#46408](https://github.com/vllm-project/vllm/pull/46408) Support invalid/non-local slots in topk_ids for Triton MoE
- [#46414](https://github.com/vllm-project/vllm/pull/46414) Fix AITER FP8 quantization schema tests on ROCm
- [#46380](https://github.com/vllm-project/vllm/pull/46380) Add MiniMax-M3 modelopt nvfp4 support
- [#46177](https://github.com/vllm-project/vllm/pull/46177) Support tensor parallelism for DiffusionGemma
- [#46389](https://github.com/vllm-project/vllm/pull/46389) Support 2/3/5/6/7-bit pack-quantized weight-only inference
- [#46549](https://github.com/vllm-project/vllm/pull/46549) Free unused MXFP4 scales in OAI Triton Backend
- [#46518](https://github.com/vllm-project/vllm/pull/46518) Allow FlashInfer MXINT4 MoE for gated SiLU
- [#46629](https://github.com/vllm-project/vllm/pull/46629) Add back emulation to available OCP MX backends list
- [#46735](https://github.com/vllm-project/vllm/pull/46735) Fix failing CUDA graph capture in Triton MOE
- [#46339](https://github.com/vllm-project/vllm/pull/46339) Re-enable FP8 MoE on NVIDIA Thor
- [#46580](https://github.com/vllm-project/vllm/pull/46580) Skip the MoE Marlin tile-padding helper assertion on ROCm
- [#46882](https://github.com/vllm-project/vllm/pull/46882) Raise gsm8k startup timeout for MoE Refactor Qwen3 NVFP4 configs
- [#46818](https://github.com/vllm-project/vllm/pull/46818) Fix incorrect layer type annotation in Fp8LinearMethod
- [#46655](https://github.com/vllm-project/vllm/pull/46655) Remove erroneous inclusion of gptq_marlin on ROCm
- [#46676](https://github.com/vllm-project/vllm/pull/46676) Add Native HIP MXFP4 for RDNA3 (opened)
- [#46871](https://github.com/vllm-project/vllm/pull/46871) Add batched MoE expert parallelism via AllGather/ReduceScatter all-to-all on XPU (opened)
- [#46901](https://github.com/vllm-project/vllm/pull/46901) Migrate int8 w4a8int8 oracle 37753 (opened)
- [#46852](https://github.com/vllm-project/vllm/pull/46852) Add ModelOpt MXFP8 small-M linear opts and env exclude-modules (opened)
- [#46739](https://github.com/vllm-project/vllm/pull/46739) Fix w4a8_int8 CPU MoE path (opened)
- [#46732](https://github.com/vllm-project/vllm/pull/46732) Integrate TokenSpeed Mxfp4 MOE Kernel (opened)
- [#46639](https://github.com/vllm-project/vllm/pull/46639) Support batch invariance for WNA16 Marlin MoE (opened)
- [#46765](https://github.com/vllm-project/vllm/pull/46765) Refactor quark_moe w8a8-int8 with oracle on ROCm (opened)
- [#46869](https://github.com/vllm-project/vllm/pull/46869) Fuse grouped_topk routing for bias-free softmax models (opened)
- [#46860](https://github.com/vllm-project/vllm/pull/46860) Fix W8A8 int-quantized scheme selection regression (opened)
- [#46816](https://github.com/vllm-project/vllm/pull/46816) Fix garbled outputs on NVFP4 MoE backends for SM 12.0a (opened)
- [#46656](https://github.com/vllm-project/vllm/pull/46656) Refactor stable ABI for MoE and quantization (opened)
- [#46845](https://github.com/vllm-project/vllm/pull/46845) Fix MiniMax-M3 compressed-tensors FP8 MoE SwiGLU params (opened)
- [#46551](https://github.com/vllm-project/vllm/pull/46551) Enable FlashInfer A2A for Minimax-M3-MXFP8 (opened)
- [#46772](https://github.com/vllm-project/vllm/pull/46772) Implement get_expert_mapping for LoRA in Gemma-4 MoE (opened)
- [#46664](https://github.com/vllm-project/vllm/pull/46664) Gate AITER MoE GateMode.INTERLEAVE on the gu-interleaved weight layout (opened)
- [#46950](https://github.com/vllm-project/vllm/pull/46950) Clear shared_experts output when forward fails (opened)
- [#46593](https://github.com/vllm-project/vllm/pull/46593) Use block_k for block-wise FP8 activation group_shape (opened)
- [#46805](https://github.com/vllm-project/vllm/pull/46805) Fix dangling temporary in AWQ gemm torch::stable::sum dim arg (opened)
- [#46880](https://github.com/vllm-project/vllm/pull/46880) Pad gated intermediate to 64 for FlashInfer TRT-LLM shuffle (opened)
- [#46894](https://github.com/vllm-project/vllm/pull/46894) Skip FlashAttnMLA + FP8 KV cache cell in test_mla_rope_kvcache_cat_fusion (opened)
- [#46795](https://github.com/vllm-project/vllm/pull/46795) Allow non-gated MoE on TPU (opened)
- [#46917](https://github.com/vllm-project/vllm/pull/46917) Guard trtllm MoE behind x86_64 check (opened)
- [#46586](https://github.com/vllm-project/vllm/pull/46586) Add note on bitsandbytes batch size dependency (opened)
- [#46944](https://github.com/vllm-project/vllm/pull/46944) Fix test_per_token_group_quant_fp8 tolerance for 1-ULP FP8 rounding on gfx950 (opened)
- [#46756](https://github.com/vllm-project/vllm/pull/46756) Add MiniMax-M3 modelopt nvfp4 support (opened)
</details>

<details>
<summary>Model support (19)</summary>

- [#46314](https://github.com/vllm-project/vllm/pull/46314) Port seed_oss to the streaming parser engine as a Qwen3 subclass
- [#46602](https://github.com/vllm-project/vllm/pull/46602) Migrate gemma4 to unified parser
- [#46564](https://github.com/vllm-project/vllm/pull/46564) Support Unlimited OCR
- [#46362](https://github.com/vllm-project/vllm/pull/46362) Remove BaiChuanForCausalLM and BaichuanForCausalLM
- [#45810](https://github.com/vllm-project/vllm/pull/45810) Add pipeline parallelism support for MiniMax-M3
- [#46605](https://github.com/vllm-project/vllm/pull/46605) Remove AquilaForCausalLM and AquilaModel
- [#46600](https://github.com/vllm-project/vllm/pull/46600) Skip indexer weights for index-cache-skipped layers in DSv3.2
- [#46316](https://github.com/vllm-project/vllm/pull/46316) Force unquantized mtp.fc for Qwen3Next to fix NVFP4+MTP crash
- [#46808](https://github.com/vllm-project/vllm/pull/46808) Add DSV3.2/GLM5 to vllm/models/
- [#46623](https://github.com/vllm-project/vllm/pull/46623) Add LongCat-Next multimodal model support (opened)
- [#46965](https://github.com/vllm-project/vllm/pull/46965) Add DeepSeek V4 DSpark speculative decoding (opened)
- [#46800](https://github.com/vllm-project/vllm/pull/46800) Add Harmony Renderer for GPT-OSS (opened)
- [#46837](https://github.com/vllm-project/vllm/pull/46837) Support ViT CUDA Graph for Gemma-4 (opened)
- [#46853](https://github.com/vllm-project/vllm/pull/46853) Add Laguna XS.2.1 DFlash drafter support (opened)
- [#46789](https://github.com/vllm-project/vllm/pull/46789) Implement Sequence Parallelism for DSV4 (opened)
- [#46788](https://github.com/vllm-project/vllm/pull/46788) Migrate EAGLE3 aux capture to EagleModelMixin for DeepSeek (opened)
- [#46632](https://github.com/vllm-project/vllm/pull/46632) Enable DSML structural tag for DeepSeek-V4 with auto + non-strict tools (opened)
- [#46730](https://github.com/vllm-project/vllm/pull/46730) Use platform FP8 dtype for Q-quant on gfx942 for DSv4 indexer (opened)
- [#46704](https://github.com/vllm-project/vllm/pull/46704) Add sycl kernel mhc path for DSv4 (opened)
- [#46766](https://github.com/vllm-project/vllm/pull/46766) Fix ModelOpt Llama-4 checkpoints taking 5+ minutes to load (opened)
</details>

<details>
<summary>Parallelism & scheduling (32)</summary>

- [#45053](https://github.com/vllm-project/vllm/pull/45053) Replace OffloadingHandler with OffloadingWorker for KV Offload
- [#46412](https://github.com/vllm-project/vllm/pull/46412) Only check and store new KV cache range for Mooncake
- [#46363](https://github.com/vllm-project/vllm/pull/46363) Replace bool|None lookup return with LookupResult enum in KV Offloading
- [#46284](https://github.com/vllm-project/vllm/pull/46284) Fix KV offload request-finished lifecycle contract
- [#45019](https://github.com/vllm-project/vllm/pull/45019) Add Mamba1 support to NIXL P/D disaggregation
- [#46855](https://github.com/vllm-project/vllm/pull/46855) Fix Mooncake lookup prefixes with DCP > 1
- [#46114](https://github.com/vllm-project/vllm/pull/46114) Fix chunk alignment when using context parallelism with TRITON_MLA
- [#46188](https://github.com/vllm-project/vllm/pull/46188) Optimize lookup pool key string construction for Mooncake
- [#46595](https://github.com/vllm-project/vllm/pull/46595) Track resumed requests via scheduler's resumed_req_ids in MooncakeStore
- [#46252](https://github.com/vllm-project/vllm/pull/46252) Gate packed HMA KV cache on cross-layer config
- [#46532](https://github.com/vllm-project/vllm/pull/46532) Throttle prefills based on local prefill work
- [#46448](https://github.com/vllm-project/vllm/pull/46448) Reduce TP communication for draft token generation
- [#46888](https://github.com/vllm-project/vllm/pull/46888) Fix tensors_per_block stride in KV-Offloading
- [#45998](https://github.com/vllm-project/vllm/pull/45998) Fix use_v2_model_runner inside Ray driver thread on ROCm
- [#46650](https://github.com/vllm-project/vllm/pull/46650) Fix Pipeline + Context Parallelism test group on AMD
- [#46628](https://github.com/vllm-project/vllm/pull/46628) Fix P/D with DP Supervisor
- [#46473](https://github.com/vllm-project/vllm/pull/46473) Disable bidirectional xfer mode for NixlPushConnector
- [#46909](https://github.com/vllm-project/vllm/pull/46909) Add AFD distributed frontend support (opened)
- [#46887](https://github.com/vllm-project/vllm/pull/46887) Remove DeepEP high-throughput backend, redirect to DeepEP v2 (opened)
- [#46889](https://github.com/vllm-project/vllm/pull/46889) Add NCCL EP all2all backend for expert parallelism (opened)
- [#46807](https://github.com/vllm-project/vllm/pull/46807) Add GDN support for PD disagg with Mooncake Connector (opened)
- [#46556](https://github.com/vllm-project/vllm/pull/46556) Add per-worker disk tier and LRU write-back for symmetric multi-node KV cache (opened)
- [#46972](https://github.com/vllm-project/vllm/pull/46972) Store interior chunk-boundary blocks under MTP/Eagle (opened)
- [#46689](https://github.com/vllm-project/vllm/pull/46689) Skip PP sampled-token broadcast on KV producer (opened)
- [#46954](https://github.com/vllm-project/vllm/pull/46954) Add canonical KV layout fields for TP-agnostic offload (opened)
- [#46960](https://github.com/vllm-project/vllm/pull/46960) Track offloading allocations without load tokens (opened)
- [#46906](https://github.com/vllm-project/vllm/pull/46906) Decouple store retention from HBM retention in KVConnector (opened)
- [#46764](https://github.com/vllm-project/vllm/pull/46764) Improve UX when FlashInfer JIT compilation is happening (opened)
- [#46898](https://github.com/vllm-project/vllm/pull/46898) Report correct cached_tokens for disaggregated prefill (opened)
- [#46777](https://github.com/vllm-project/vllm/pull/46777) Merge kv_transfer_params dicts across connectors (opened)
- [#46626](https://github.com/vllm-project/vllm/pull/46626) Fix DP supervisor (opened)
- [#46824](https://github.com/vllm-project/vllm/pull/46824) Fix decode-phase blocks not stored in CPU KV cache offloading (opened)
</details>

<details>
<summary>Hardware & arch (19)</summary>

- [#44465](https://github.com/vllm-project/vllm/pull/44465) Add VRAM semaphore infra for NVIDIA
- [#44551](https://github.com/vllm-project/vllm/pull/44551) Correct reasoning-end detection for prompt history on NVIDIA
- [#46202](https://github.com/vllm-project/vllm/pull/46202) Enable chunked prefill and prefix caching for qwen3.5 on CPU
- [#45269](https://github.com/vllm-project/vllm/pull/45269) Add RVV path for W4A8 INT4 GEMM on CPU
- [#45850](https://github.com/vllm-project/vllm/pull/45850) Use background thread for mmap / cpu_tensors pinning on CPU
- [#46769](https://github.com/vllm-project/vllm/pull/46769) Fix macOS/Apple Silicon hang by enabling OpenMP in the build
- [#46636](https://github.com/vllm-project/vllm/pull/46636) Begin deprecation window for CUDA_VISIBLE_DEVICES on ROCm
- [#46101](https://github.com/vllm-project/vllm/pull/46101) Normalize slashes in Helion GPU names
- [#46495](https://github.com/vllm-project/vllm/pull/46495) Fix NemotronLayerNorm1P hardcoded cuda device type
- [#46699](https://github.com/vllm-project/vllm/pull/46699) Add gfx950 HIP compressor path for DSV4 on ROCm (opened)
- [#46904](https://github.com/vllm-project/vllm/pull/46904) Refresh ROCm base images when docker rocm_base changes (opened)
- [#46877](https://github.com/vllm-project/vllm/pull/46877) Add GPU worker checkpoint hooks for NVIDIA (opened)
- [#46682](https://github.com/vllm-project/vllm/pull/46682) Add helion nvfp4 backend for batch_size=1 (opened)
- [#46959](https://github.com/vllm-project/vllm/pull/46959) Check CPU KV offload shared-memory capacity (opened)
- [#46932](https://github.com/vllm-project/vllm/pull/46932) Fix negative CUDA graph memory estimate on unified-memory GPUs (opened)
- [#46697](https://github.com/vllm-project/vllm/pull/46697) Add CPU fallback for mamba batch memcpy (opened)
- [#46681](https://github.com/vllm-project/vllm/pull/46681) Disable packed KV cache allocation on XPU for DeepSeek-V4 (opened)
- [#46907](https://github.com/vllm-project/vllm/pull/46907) Build cpu_fused_moe on Apple Silicon (opened)
- [#46821](https://github.com/vllm-project/vllm/pull/46821) Detect APUs so memory budget uses VRAM, not system RAM on ROCm (opened)
</details>

<details>
<summary>API & serving (54)</summary>

- [#44124](https://github.com/vllm-project/vllm/pull/44124) Support OpenMOSS-Team
- [#46584](https://github.com/vllm-project/vllm/pull/46584) Make ToolParserOutput a seq of ToolParserEvent to preserve order
- [#46719](https://github.com/vllm-project/vllm/pull/46719) Extract renderer fixture test utilities
- [#46344](https://github.com/vllm-project/vllm/pull/46344) Fix Kimi K2 tool call IDs for required tool choice
- [#46057](https://github.com/vllm-project/vllm/pull/46057) Integrate xgrammar-structural-tag for strict and required tool calling
- [#44226](https://github.com/vllm-project/vllm/pull/44226) Add token offsets to render endpoints
- [#46799](https://github.com/vllm-project/vllm/pull/46799) Use oss-harmony for Harmony output processing
- [#46846](https://github.com/vllm-project/vllm/pull/46846) Add return_loss_mask to render endpoint for training data generation
- [#46535](https://github.com/vllm-project/vllm/pull/46535) Support EVS in Model Runner V2
- [#46507](https://github.com/vllm-project/vllm/pull/46507) Make Granite4 string argument scanning incremental
- [#46486](https://github.com/vllm-project/vllm/pull/46486) Fix string whitespace and required named tool choice for PoolsideV1
- [#46782](https://github.com/vllm-project/vllm/pull/46782) Fix chunked embedding aggregation with request-id metadata
- [#46360](https://github.com/vllm-project/vllm/pull/46360) Pass effective reasoning_parser_kwargs for structured output
- [#46733](https://github.com/vllm-project/vllm/pull/46733) Reject min_tokens above max_tokens
- [#46437](https://github.com/vllm-project/vllm/pull/46437) Use process_eos() to flush Harmony Parser outputs
- [#46776](https://github.com/vllm-project/vllm/pull/46776) Deduplicate ModelState init logic
- [#46762](https://github.com/vllm-project/vllm/pull/46762) Support realtime embeddings in ModelRunner V2
- [#46775](https://github.com/vllm-project/vllm/pull/46775) Add flag to print TTFT and TPS in vllm chat
- [#46382](https://github.com/vllm-project/vllm/pull/46382) Fix stream Mimimax m2 tool call string arguments
- [#46525](https://github.com/vllm-project/vllm/pull/46525) Emit a content block for empty Anthropic completions
- [#46582](https://github.com/vllm-project/vllm/pull/46582) Raise frontend JSON body limit
- [#46783](https://github.com/vllm-project/vllm/pull/46783) Move the legacy api_server.py to the examples directory
- [#46843](https://github.com/vllm-project/vllm/pull/46843) Pass token IDs to parser.parse() in Responses API and batch serving
- [#46823](https://github.com/vllm-project/vllm/pull/46823) Fix transcription flakiness in AMD Entrypoints Integration
- [#46768](https://github.com/vllm-project/vllm/pull/46768) Add per-request timing metrics field to response body (opened)
- [#46610](https://github.com/vllm-project/vllm/pull/46610) Add Streaming Parser Engine and new Kimi k2.5/k2.6/k2.7 Parser (opened)
- [#46813](https://github.com/vllm-project/vllm/pull/46813) Add Rust Apertus tool parser (opened)
- [#46727](https://github.com/vllm-project/vllm/pull/46727) Support thinking_token_budget in Model Runner V2 (opened)
- [#46617](https://github.com/vllm-project/vllm/pull/46617) Add Jamba tool parser (opened)
- [#46926](https://github.com/vllm-project/vllm/pull/46926) Add idle timeout for /v1/realtime audio sessions (opened)
- [#46814](https://github.com/vllm-project/vllm/pull/46814) Add idle watchdog for audio WebSocket sessions (opened)
- [#46811](https://github.com/vllm-project/vllm/pull/46811) Add low-overhead /ready GPU health check (opened)
- [#46709](https://github.com/vllm-project/vllm/pull/46709) Add longcat tool parser support (opened)
- [#46921](https://github.com/vllm-project/vllm/pull/46921) Package example Jinja chat templates in wheels (opened)
- [#46723](https://github.com/vllm-project/vllm/pull/46723) Avoid redundant decode per token in incremental detokenizer (opened)
- [#46680](https://github.com/vllm-project/vllm/pull/46680) Support srt response format for audio transcription (opened)
- [#46833](https://github.com/vllm-project/vllm/pull/46833) Start current wave for a stale DP FirstRequest (opened)
- [#46677](https://github.com/vllm-project/vllm/pull/46677) Accept chat-completions image format on /v1/responses (opened)
- [#46784](https://github.com/vllm-project/vllm/pull/46784) Unflatten namespace tool names before returning function calls (opened)
- [#46663](https://github.com/vllm-project/vllm/pull/46663) Fix reasoning-end detection to check prompt tail only (opened)
- [#46684](https://github.com/vllm-project/vllm/pull/46684) Add repetition_detection support to sampling params across Rust frontend (opened)
- [#46797](https://github.com/vllm-project/vllm/pull/46797) Accept server tools without input_schema for Anthropic (opened)
- [#46744](https://github.com/vllm-project/vllm/pull/46744) Support cache_salt in the Anthropic Messages API (opened)
- [#46934](https://github.com/vllm-project/vllm/pull/46934) Fix granite4 streaming dropping content after a single-delta tool call (opened)
- [#46829](https://github.com/vllm-project/vllm/pull/46829) Suppress whitespace-only deltas in DeepSeek tool parsing (opened)
- [#46890](https://github.com/vllm-project/vllm/pull/46890) Parse JSON tool calls in Llama 4 pythonic parser (opened)
- [#46827](https://github.com/vllm-project/vllm/pull/46827) Keep literal "null" string for string-typed tool params (opened)
- [#46793](https://github.com/vllm-project/vllm/pull/46793) Support bad_words in the /v1/completions endpoint (opened)
- [#46939](https://github.com/vllm-project/vllm/pull/46939) Forward request-level prompt extras for cross-encoder scoring (opened)
- [#46612](https://github.com/vllm-project/vllm/pull/46612) Raise VLLMValidationError for non-integer logit_bias keys (opened)
- [#46616](https://github.com/vllm-project/vllm/pull/46616) Balance MiniMax M3 reasoning markers in is_reasoning_end (opened)
- [#46614](https://github.com/vllm-project/vllm/pull/46614) Parse compact sentence-transformers pooling_mode (opened)
- [#46708](https://github.com/vllm-project/vllm/pull/46708) Fix make_valid_python backslash-escape edge case (opened)
- [#46966](https://github.com/vllm-project/vllm/pull/46966) Validate Pooling cache_salt Values (opened)
- [#46779](https://github.com/vllm-project/vllm/pull/46779) Fix incorrect CLI arg validation tests (opened)
</details>

<details>
<summary>Speculative Decoding (15)</summary>

- [#46786](https://github.com/vllm-project/vllm/pull/46786) Handle tuple hidden states from MTP draft models
- [#46560](https://github.com/vllm-project/vllm/pull/46560) Fix int32 offset overflow in sampler kernels
- [#46533](https://github.com/vllm-project/vllm/pull/46533) Reject placeholder (-1) draft tokens in rejection sampler
- [#45956](https://github.com/vllm-project/vllm/pull/45956) Fix probabilistic sampling for parallel drafting
- [#46878](https://github.com/vllm-project/vllm/pull/46878) Use fp32 uniform threshold for acceptance
- [#46488](https://github.com/vllm-project/vllm/pull/46488) Propagate norm_output and fc_norm config for Eagle3 speculators
- [#46770](https://github.com/vllm-project/vllm/pull/46770) Enable dflash attention backend selection
- [#46781](https://github.com/vllm-project/vllm/pull/46781) Implement block verification for rejection sampling (opened)
- [#46725](https://github.com/vllm-project/vllm/pull/46725) Add runtime draft weight update for speculative decoding (opened)
- [#46897](https://github.com/vllm-project/vllm/pull/46897) Add unit tests for metrics and custom proposer loader (opened)
- [#46574](https://github.com/vllm-project/vllm/pull/46574) Sanitize invalid speculative draft tokens (opened)
- [#46947](https://github.com/vllm-project/vllm/pull/46947) Clamp negative placeholder token ids before multimodal text embedding (opened)
- [#46899](https://github.com/vllm-project/vllm/pull/46899) Clear stale async speculative placeholders (opened)
- [#46694](https://github.com/vllm-project/vllm/pull/46694) Fix NIXL async KV load lookahead handling for MTP spec decode (opened)
- [#46662](https://github.com/vllm-project/vllm/pull/46662) Fix spec tb combine overhead (opened)
</details>

<details>
<summary>Multimodal (15)</summary>

- [#46034](https://github.com/vllm-project/vllm/pull/46034) Enable dual-path ViT CUDA graph for Step3-VL
- [#46705](https://github.com/vllm-project/vllm/pull/46705) Migrate Voxtral to mistral-common 1.11.5 audio API
- [#46552](https://github.com/vllm-project/vllm/pull/46552) Recompute mm_token_type_ids per request for M-RoPE
- [#45263](https://github.com/vllm-project/vllm/pull/45263) Fix relative allowed local media paths
- [#46741](https://github.com/vllm-project/vllm/pull/46741) Fix HIP fork re-init in multimodal offline examples
- [#46467](https://github.com/vllm-project/vllm/pull/46467) Fix duplicated logging when loading a corrupt or partial video
- [#46749](https://github.com/vllm-project/vllm/pull/46749) Spawn engine in mm cache sleep test to fix ROCm HIP error
- [#46653](https://github.com/vllm-project/vllm/pull/46653) DO NOT MERGE (opened)
- [#46836](https://github.com/vllm-project/vllm/pull/46836) Fix oversized video inputs in multimodal loader (opened)
- [#46609](https://github.com/vllm-project/vllm/pull/46609) Add TorchCodec as a video decoding backend (opened)
- [#46747](https://github.com/vllm-project/vllm/pull/46747) Recover from P0/P1 processor cache drift (opened)
- [#46942](https://github.com/vllm-project/vllm/pull/46942) Enable mm prefix bidi attention support on MRV2 (opened)
- [#46606](https://github.com/vllm-project/vllm/pull/46606) Support Vit CudaGraph for v2 (opened)
- [#46957](https://github.com/vllm-project/vllm/pull/46957) Fix Qwen3-VL video prompt wrapper replacement (opened)
- [#46630](https://github.com/vllm-project/vllm/pull/46630) Resolve unquantized embedding method and key mismatch in inc path for MiniMax-M3 (opened)
</details>

<details>
<summary>Tests, CI & build (42)</summary>

- [#46590](https://github.com/vllm-project/vllm/pull/46590) Add intel full ci job yamls (opened)
- [#46844](https://github.com/vllm-project/vllm/pull/46844) Add Mooncake PD integration tests (opened)
- [#46902](https://github.com/vllm-project/vllm/pull/46902) Bump the minor-update group across 1 directory with 149 updates (opened)
- [#46660](https://github.com/vllm-project/vllm/pull/46660) Build macOS arm64 CPU wheels via GitHub-hosted runners (opened)
- [#46711](https://github.com/vllm-project/vllm/pull/46711) Add registry layer cache to x86 CUDA release image builds (opened)
- [#46599](https://github.com/vllm-project/vllm/pull/46599) Rename Docker build stages for clarity (opened)
- [#46683](https://github.com/vllm-project/vllm/pull/46683) Bump flashinfer version to 0.6.13 (opened)
- [#46868](https://github.com/vllm-project/vllm/pull/46868) Improve InstantTensor loading (opened)
- [#46870](https://github.com/vllm-project/vllm/pull/46870) Remove stray duplicate from serving benchmark config (opened)
- [#46587](https://github.com/vllm-project/vllm/pull/46587) Fix XPU UT failure by using platform-aware imports (opened)
- [#46964](https://github.com/vllm-project/vllm/pull/46964) Bump xgrammar to fix structural-tag test (opened)
- [#46893](https://github.com/vllm-project/vllm/pull/46893) Add GSM8K eval integration test for KV offloading (opened)
- [#46713](https://github.com/vllm-project/vllm/pull/46713) Batch Lookup in C for FS-Offloading (opened)
- plus 29 more minor CI and test updates
</details>

<details>
<summary>Bugfixes (29)</summary>

- [#44483](https://github.com/vllm-project/vllm/pull/44483) Fix illegal memory access from a forward during a partial wake_up
- [#46220](https://github.com/vllm-project/vllm/pull/46220) Keep pydantic validation for fields with a TYPE_CHECKING Literal alias
- [#46506](https://github.com/vllm-project/vllm/pull/46506) Fix FLASHINFER_MLA_SPARSE_SM120 compatibility with GLM-5 NVFP4
- [#46627](https://github.com/vllm-project/vllm/pull/46627) Fix IndentationError expected an indented block after with statement
- [#46773](https://github.com/vllm-project/vllm/pull/46773) Fix whisper test in ModelRunner V2
- [#44984](https://github.com/vllm-project/vllm/pull/44984) Eliminate race conditions in shared buildkit cache mounts
- [#46851](https://github.com/vllm-project/vllm/pull/46851) Fix rlhf_nccl.py on ROCm
- [#46915](https://github.com/vllm-project/vllm/pull/46915) Fix test_flashinfer_cutlass_mxfp4_fused_moe on sm90
- [#46841](https://github.com/vllm-project/vllm/pull/46841) Fix request-bound KV cache sizing (opened)
- [#46734](https://github.com/vllm-project/vllm/pull/46734) Patch getpass.getuser() for arbitrary-UID containers (opened)
- [#46652](https://github.com/vllm-project/vllm/pull/46652) Calculate ITL using exact token delta from usage stats (opened)
- [#46700](https://github.com/vllm-project/vllm/pull/46700) Cap repetition_detection window to bound scheduler CPU (opened)
- [#46874](https://github.com/vllm-project/vllm/pull/46874) Fix moriio completion notification (opened)
- [#46690](https://github.com/vllm-project/vllm/pull/46690) Fix UVA offload fallback copies (opened)
- [#46840](https://github.com/vllm-project/vllm/pull/46840) Validate sparse MLA top-k buffer on SM120 (opened)
- [#46839](https://github.com/vllm-project/vllm/pull/46839) Reject prompt_logprobs for streaming generate (opened)
- [#46892](https://github.com/vllm-project/vllm/pull/46892) Fix get_num_blocks_to_allocate providing wrong block count (opened)
- [#46962](https://github.com/vllm-project/vllm/pull/46962) Add buffer-length check in shm.cpp (opened)
- [#46885](https://github.com/vllm-project/vllm/pull/46885) Revert Support tensor parallelism for DiffusionGemma (opened)
- [#46554](https://github.com/vllm-project/vllm/pull/46554) Lazy-grow InputBatch token_ids_cpu / is_token_ids buffers (opened)
- [#46835](https://github.com/vllm-project/vllm/pull/46835) Apply learned lm_head.bias for tied-embedding models in Transformers backend (opened)
- [#46567](https://github.com/vllm-project/vllm/pull/46567) Fix model info cache for package models (opened)
- [#46920](https://github.com/vllm-project/vllm/pull/46920) Skip unknown metric types in get_metrics_snapshot (opened)
- [#46953](https://github.com/vllm-project/vllm/pull/46953) Fix hf3fs kv connector md5 hashing (opened)
- [#46757](https://github.com/vllm-project/vllm/pull/46757) Fix Quark mxfp4 quantized model loading issue under mtp (opened)
- [#46714](https://github.com/vllm-project/vllm/pull/46714) Fix misleading docstrings in non-impacting config compute_hash (opened)
- [#46970](https://github.com/vllm-project/vllm/pull/46970) Resolve local refs for tool argument coercion (opened)
- [#46925](https://github.com/vllm-project/vllm/pull/46925) Resolve $ref/$defs in tool schemas before type coercion (opened)
- [#46958](https://github.com/vllm-project/vllm/pull/46958) Revert Use background thread for mmap / cpu_tensors pinning (opened)
</details>

<details>
<summary>Docs & Misc (23)</summary>

- [#44800](https://github.com/vllm-project/vllm/pull/44800) Add VLLM_GPU_SYNC_CHECK env var
- [#46771](https://github.com/vllm-project/vllm/pull/46771) Update scheduler tests to cover MRV2 paths
- [#46511](https://github.com/vllm-project/vllm/pull/46511) Update to log once
- [#44610](https://github.com/vllm-project/vllm/pull/44610) Forward VLLM_ENGINE_READY_TIMEOUT_S via --args-json
- [#46746](https://github.com/vllm-project/vllm/pull/46746) Bound memory for large logprobs requests
- [#36701](https://github.com/vllm-project/vllm/pull/36701) Remove FlashAttention block size restriction for hybrid models
- [#40469](https://github.com/vllm-project/vllm/pull/40469) Fix minor doc sentence, grammar, quote errors
- [#44720](https://github.com/vllm-project/vllm/pull/44720) Document Qwen3.6 ViT CUDA graph support
- [#46071](https://github.com/vllm-project/vllm/pull/46071) Remove BambaForCausalLM from supported hybrid models list
- [#46969](https://github.com/vllm-project/vllm/pull/46969) Remove tool_parsers/gemma4_utils.py in favor of Transformers v5 chat parsing API (opened)
- [#46647](https://github.com/vllm-project/vllm/pull/46647) Move iteration logging to the frontend (opened)
- [#46698](https://github.com/vllm-project/vllm/pull/46698) Releases/v0.22.1 (opened)
- [#46718](https://github.com/vllm-project/vllm/pull/46718) Add runtime monitor for post-warmup TileLang compilation (opened)
- [#46575](https://github.com/vllm-project/vllm/pull/46575) Add deferred wait time histogram (opened)
- [#46938](https://github.com/vllm-project/vllm/pull/46938) Report prefix cache hit rate in vllm bench serve (opened)
- [#46828](https://github.com/vllm-project/vllm/pull/46828) Add post-load weight processing registry (opened)
- [#46621](https://github.com/vllm-project/vllm/pull/46621) Improve Triton JIT diagnostics (opened)
- [#46806](https://github.com/vllm-project/vllm/pull/46806) Remove mantis (opened)
- [#46864](https://github.com/vllm-project/vllm/pull/46864) Manual activation+quant fusion via QuantizedActivation (opened)
- [#46598](https://github.com/vllm-project/vllm/pull/46598) Add remediation hints to MTP and PCP context-parallel errors (opened)
- [#46956](https://github.com/vllm-project/vllm/pull/46956) Remove boilerplate missed by [#46820](https://github.com/vllm-project/vllm/pull/46820) (opened)
- [#46875](https://github.com/vllm-project/vllm/pull/46875) Auto-drop special tokens via tokenizer discovery (opened)
- [#46922](https://github.com/vllm-project/vllm/pull/46922) Add OpenAI server production hardening checklist (opened)
</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (vllm.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
