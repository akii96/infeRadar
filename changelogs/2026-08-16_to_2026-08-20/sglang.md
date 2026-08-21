# sglang: PR digest (2026-08-16 to 2026-08-20)

_272 merged, 404 newly opened - source sgl-project/sglang, generated 2026-08-20T09:57:11Z_

## TL;DR
- **Model Focus:** DeepSeek (V4, DSpark) and MiniMax (H3) dominated this window, followed by GLM-5.2, Qwen, and Kimi-K3. Diffusion models (Hunyuan3D, Cosmos3, Sana) also saw heavy feature work.
- **Performance & Kernels:** Massive investments in FP8/MXFP4 quantization and MoE routing, highlighted by a new Cake batch DeepGEMM backend and DeepEPv2 MoE A2A integration.
- **Memory & Caching:** Major enhancements to HiCache (buffer-only mode, DCP support) and unified memory architectures, alongside process-local in-memory KV indexing.
- **Hardware Expansion:** Broad hardware optimization, notably for AMD (ROCm 7.2.4, gfx950, MI355X), Ascend NPUs (DeepSeek-V4 DSpark, GLM-5), and Intel XPU.
- **Overall Direction:** The engine is heavily optimizing for low-latency, high-throughput serving of massive MoE and multimodal models through aggressive kernel fusion, advanced speculative decoding (DFlash2, EAGLE), and unified KV cache management.

## Most important PRs
- **[#35369](https://github.com/sgl-project/sglang/pull/35369) feat(cake_gemm): add Cake batch DeepGEMM FP8 backend**
  Introduces a massive new FP8 DeepGEMM backend (Cake) to accelerate batch matrix multiplications across multiple hardware targets.
- **[#33370](https://github.com/sgl-project/sglang/pull/33370) [Feature] Add process-local in-memory KV indexer and Router integration**
  Implements a process-local KV indexer to drastically reduce routing overhead and improve memory management for large-scale deployments.
- **[#35309](https://github.com/sgl-project/sglang/pull/35309) [Feat][GLM-5.2] Shared KV Cache for Prefill and Decode**
  Unifies the KV cache architecture for GLM-5.2, allowing prefill and decode phases to share memory and improve overall throughput.
- **[#33676](https://github.com/sgl-project/sglang/pull/33676) [NPU] Support DeepSeek-V4 DSpark and refactor DSV4 cache management**
  Brings DeepSeek-V4 DSpark support to Ascend NPUs while overhauling the model's cache management for better distributed performance.
- **[#35114](https://github.com/sgl-project/sglang/pull/35114) [kernels] Reorganize ops/diffusion by operator domain behind a lazy facade**
  Refactors the diffusion operator library into a lazy-loaded, domain-driven architecture to speed up startup and clean up the kernel namespace.

## More changes by area

<details>
<summary>Performance (21)</summary>

- [#35016](https://github.com/sgl-project/sglang/pull/35016) tighten NVIDIA perf baselines for diffusion
- [#35381](https://github.com/sgl-project/sglang/pull/35381) NPU GLM 5 optim pp cp
- [#35318](https://github.com/sgl-project/sglang/pull/35318) PaddleOCR-VL: overlap page preprocessing, pack ViT, enable prefill CUDA graph
- [#33880](https://github.com/sgl-project/sglang/pull/33880) reduce MiniMax H3 MPS memory pressure
- [#35559](https://github.com/sgl-project/sglang/pull/35559) NPU GLM 5 optim pp cp bug fix
- [#35061](https://github.com/sgl-project/sglang/pull/35061) select custom all-reduce v2 by topology capability
- [#34890](https://github.com/sgl-project/sglang/pull/34890) hoist DSv4 draft-extend SWA write locs; unify SWA graph buffer naming
- [#35560](https://github.com/sgl-project/sglang/pull/35560) NPU GLM 5 optim bug fix
- [#35207](https://github.com/sgl-project/sglang/pull/35207) reduce host-side overhead in ngram draft prep
- [#35287](https://github.com/sgl-project/sglang/pull/35287) AMD Perf Kimi-K3 low concurrency optimizations
- [#35335](https://github.com/sgl-project/sglang/pull/35335) warmup-calibrated auto residency promotion in performance-mode auto
- [#35098](https://github.com/sgl-project/sglang/pull/35098) overlap front-end via direct TopK output for DSV4 MegaMoE
- [#35074](https://github.com/sgl-project/sglang/pull/35074) AMD Perf dsv4 enable heterogeneous AITER FHMoE
- [#35681](https://github.com/sgl-project/sglang/pull/35681) avoid RadixKey suffix copies in cache walks
- [#35308](https://github.com/sgl-project/sglang/pull/35308) AMD Perf Kimi-K3 fuse MLA Q and cache preparation
- [#35268](https://github.com/sgl-project/sglang/pull/35268) avoid full-logits all-gather for TP greedy sampling
- [#35142](https://github.com/sgl-project/sglang/pull/35142) fuse FA3 query quantization with RoPE
- [#35192](https://github.com/sgl-project/sglang/pull/35192) 2shot_lamport custom all-reduce for the 1–8 MB band
- [#35246](https://github.com/sgl-project/sglang/pull/35246) memoize Req.tail_str to halve stop-string decode calls per step
- [#35315](https://github.com/sgl-project/sglang/pull/35315) evaluate enc-dec cuda-graph gate on encoder_lens_cpu mirror
- [#35448](https://github.com/sgl-project/sglang/pull/35448) keep RadixKey prefix matching on the array('q') memcmp path
</details>

<details>
<summary>Kernels & attention (37)</summary>

- [#35031](https://github.com/sgl-project/sglang/pull/35031) migrate causal_conv1d_fwd and causal_conv1d_update from AOT to JIT
- [#34580](https://github.com/sgl-project/sglang/pull/34580) optimize KIMI-K3 with Triton MLA decode kernel by tuning stage-1 geometry for gfx950
- [#34680](https://github.com/sgl-project/sglang/pull/34680) support subblock sparse attention on SM90 for MiniMax H3
- [#34949](https://github.com/sgl-project/sglang/pull/34949) route MiniMax H3 VAE attention through native backends
- [#35041](https://github.com/sgl-project/sglang/pull/35041) trim top-k v2 output modes and tighten its PDL waits
- [#34928](https://github.com/sgl-project/sglang/pull/34928) accelerate Sana BCG with bit-exact conv post-processing
- [#33313](https://github.com/sgl-project/sglang/pull/33313) route decode wo_a bf16 batched matmul to aiter batched_gemm_bf16 for DeepSeek-V4
- [#35336](https://github.com/sgl-project/sglang/pull/35336) feed packed qkv projection output to vision backends uncopied
- [#34277](https://github.com/sgl-project/sglang/pull/34277) emit TMA-aligned UE8M0 scales for FP8 einsum
- [#34932](https://github.com/sgl-project/sglang/pull/34932) accelerate Cosmos3 T2I QKNorm+RoPE
- [#34921](https://github.com/sgl-project/sglang/pull/34921) suppress expected FlashInfer TRT-LLM workspace warnings
- [#35084](https://github.com/sgl-project/sglang/pull/35084) drop prefill index-selection syncs by taking each rank's rows by stride
- [#34888](https://github.com/sgl-project/sglang/pull/34888) split TRTLLM MHA decode batches by KV sequence length
- [#23112](https://github.com/sgl-project/sglang/pull/23112) add fmha_v2 attention backend for SM90/120
- [#31324](https://github.com/sgl-project/sglang/pull/31324) skip DSA decode indexer when kv_len <= index_topk
- [#35078](https://github.com/sgl-project/sglang/pull/35078) MXFP4 (E2M1+E8M0) KV cache for Ampere sm86: quantization + fused decode kernels [WIP]
- [#35429](https://github.com/sgl-project/sglang/pull/35429) add SM80 Torch fallbacks and Triton paged-MQA indexer
- [#35155](https://github.com/sgl-project/sglang/pull/35155) fire compress+norm+rope fusion under MTP for DSv4
- [#35444](https://github.com/sgl-project/sglang/pull/35444) add strict FlashInfer SSD and Cake prefill backends for Mamba
- [#35151](https://github.com/sgl-project/sglang/pull/35151) add support for new quantized attention backends for GFX950
- [#35226](https://github.com/sgl-project/sglang/pull/35226) support Kimi K3 prefill context parallel on NPU
- [#35322](https://github.com/sgl-project/sglang/pull/35322) use flashinfer native fp8 MLA on SM90 instead of per-layer full-pool bf16 cast
- [#35523](https://github.com/sgl-project/sglang/pull/35523) moonmath MLA attention backend: MLA decode and speculative verify on gfx942
- [#35684](https://github.com/sgl-project/sglang/pull/35684) MiniMax-H3 Spectrum skip-step + fused RMSNorm/AdaLN
- [#35657](https://github.com/sgl-project/sglang/pull/35657) add FlashInfer TRTLLM-GEN block-sparse decode attention for MiniMax-M3
- [#35400](https://github.com/sgl-project/sglang/pull/35400) route Qwen TP4 decode and verify rows through Cake
- [#35417](https://github.com/sgl-project/sglang/pull/35417) use Cake source Router GEMM for DeepSeek, GLM, and Mistral
- [#35428](https://github.com/sgl-project/sglang/pull/35428) fix gfx950 Triton compiler crash on fp8 KV-cache attention
- [#35521](https://github.com/sgl-project/sglang/pull/35521) split-KV verify on gfx942: CU-aware split cap, bidirectional draft blocks
- [#35522](https://github.com/sgl-project/sglang/pull/35522) enable chunked prefix KV on the aiter backend
- [#35021](https://github.com/sgl-project/sglang/pull/35021) add causal conv1d for ascend kda backend
- [#35095](https://github.com/sgl-project/sglang/pull/35095) DSv4 top-k v2: raw_indices output + adaptive cluster split
- [#35555](https://github.com/sgl-project/sglang/pull/35555) migrate FlashInfer MLA to unified planning and tensor APIs
- [#35171](https://github.com/sgl-project/sglang/pull/35171) extend RoPE cos/sin cache with subclass inv_freq and row scaling
- [#35175](https://github.com/sgl-project/sglang/pull/35175) route ragged prefill top-k to v2 kernel
- [#35640](https://github.com/sgl-project/sglang/pull/35640) coordinate FullCG prefill across DP-attention ranks
- [#35292](https://github.com/sgl-project/sglang/pull/35292) boot Inkling on Hopper without an explicit attention backend
</details>

<details>
<summary>MoE & quantization (49)</summary>

- [#29525](https://github.com/sgl-project/sglang/pull/29525) add DeepEPv2 (ElasticBuffer) MoE A2A backend
- [#35568](https://github.com/sgl-project/sglang/pull/35568) revert "[Feature] Add DeepEPv2 (ElasticBuffer) MoE A2A backend"
- [#32327](https://github.com/sgl-project/sglang/pull/32327) add Q8KV8 sparse MLA prefill runtime backend for DeepSeek-V4
- [#34509](https://github.com/sgl-project/sglang/pull/34509) migrate moe_topk_softmax from AOT to JIT
- [#34581](https://github.com/sgl-project/sglang/pull/34581) optimizing MiniMax-H3 for consumer-level GPUs: INT8 Linear + pluggable DiT attention backends
- [#34986](https://github.com/sgl-project/sglang/pull/34986) load quantized H3 text encoder checkpoints
- [#35172](https://github.com/sgl-project/sglang/pull/35172) extract shared checkpoint quant metadata resolver
- [#32340](https://github.com/sgl-project/sglang/pull/32340) Amd/dsv4 shared experts fusion top6
- [#33165](https://github.com/sgl-project/sglang/pull/33165) eliminate bpreshuffle fp8-scale relayout copy in dense w8a8 linear for DeepSeek-V4 MI355X
- [#35228](https://github.com/sgl-project/sglang/pull/35228) load compressed-tensors quantized lm_head instead of value-casting it
- [#35077](https://github.com/sgl-project/sglang/pull/35077) support Kimi-K3 ModelOpt mixed NVFP4/FP8 checkpoint
- [#30318](https://github.com/sgl-project/sglang/pull/30318) add mxfp4-w4a8 MOE Quantization Support for NPU
- [#30319](https://github.com/sgl-project/sglang/pull/30319) add mxfp4-w4a4 MOE Quantization Support for NPU
- [#34327](https://github.com/sgl-project/sglang/pull/34327) extend NVFP4 Marlin tests to SM120
- [#34908](https://github.com/sgl-project/sglang/pull/34908) support Intern-S2-Mobius FP8
- [#31323](https://github.com/sgl-project/sglang/pull/31323) fuse shared-expert append into aiter grouped-topk
- [#35105](https://github.com/sgl-project/sglang/pull/35105) revert "[AMD] [GLM5] Fuse shared-expert append into aiter grouped-topk"
- [#35353](https://github.com/sgl-project/sglang/pull/35353) make --vae-tiling honest, fix decode OOM advice, gate NVFP4 on Blackwell
- [#34795](https://github.com/sgl-project/sglang/pull/34795) add H20 fp8_w8a8 tuned configs for Qwen3.8 + fix Qwen3_5MoeForCausalLM tuning
- [#35162](https://github.com/sgl-project/sglang/pull/35162) add deepseek_v4_flash_w8a8_8p_in32k_out1k_50ms
- [#35372](https://github.com/sgl-project/sglang/pull/35372) support wider rows in mega_moe_pre_dispatch
- [#35593](https://github.com/sgl-project/sglang/pull/35593) support 128-aligned hidden sizes in W4AFP8 DeepEP low-latency requant kernel
- [#35200](https://github.com/sgl-project/sglang/pull/35200) fix Quark Shared Experts Fusion Gate after load-time-override Removal
- [#34962](https://github.com/sgl-project/sglang/pull/34962) fix GPTQ scheme attachment broken by LinearBase.scheme default
- [#31370](https://github.com/sgl-project/sglang/pull/31370) fold padded-topk_ids fill into fused shared-experts append+remap
- [#30900](https://github.com/sgl-project/sglang/pull/30900) fix bug related to fp8 max on gfx95x for per-token-group quant
- [#35020](https://github.com/sgl-project/sglang/pull/35020) correct dense FP8 Marlin bias ordering
- [#35194](https://github.com/sgl-project/sglang/pull/35194) update Qwen3.5 H200 FP8 for AgentX HiCache MTP
- [#34923](https://github.com/sgl-project/sglang/pull/34923) apply latest DeepEP branch
- [#30519](https://github.com/sgl-project/sglang/pull/30519) fp8 MLA absorbed bmm for GLM-5.2 on gfx950
- [#35634](https://github.com/sgl-project/sglang/pull/35634) add DeepEPv2 (ElasticBuffer) MoE A2A backend
- [#35459](https://github.com/sgl-project/sglang/pull/35459) MXFP8 x BF16 MegaMOE support
- [#35087](https://github.com/sgl-project/sglang/pull/35087) add H200 GLM-4.5 fused MoE fast path
- [#35525](https://github.com/sgl-project/sglang/pull/35525) MXFP4 MoE on gfx942 through aiter's Triton kernels
- [#35619](https://github.com/sgl-project/sglang/pull/35619) integrate Aiter MegaMoEv2 for DeepSeek-V4
- [#35180](https://github.com/sgl-project/sglang/pull/35180) share bounded post-load device staging
- [#35535](https://github.com/sgl-project/sglang/pull/35535) fix replicated (TP1) shared expert being summed by collectives that skip MoE all-reduce
- [#35461](https://github.com/sgl-project/sglang/pull/35461) support Kimi-K3 FlashInfer MXFP4 MoE on SM120
- [#35120](https://github.com/sgl-project/sglang/pull/35120) add FlashInfer CuTe DSL NVFP4 W4A16 mode
- [#35441](https://github.com/sgl-project/sglang/pull/35441) add mxfp scheme support for AR
- [#35351](https://github.com/sgl-project/sglang/pull/35351) skip writes to reserved CUDA-graph padding slot for mxfp8-kv
- [#35232](https://github.com/sgl-project/sglang/pull/35232) support FP32 MoE Router Weights on AMX
- [#35405](https://github.com/sgl-project/sglang/pull/35405) fix SM107 MXFP8 activation prep
- [#35374](https://github.com/sgl-project/sglang/pull/35374) add H200 MoE configs for recent Qwen models
- [#35406](https://github.com/sgl-project/sglang/pull/35406) Kimi-K3 MoE front optimization
- [#35163](https://github.com/sgl-project/sglang/pull/35163) fix shared expert under-weighted when rsf is pre-folded in topk weights
- [#35073](https://github.com/sgl-project/sglang/pull/35073) support GLM ModelOpt NVFP4 with Humming on Hopper
- [#35113](https://github.com/sgl-project/sglang/pull/35113) reland: Fuse shared-expert append into aiter grouped-topk
- [#35123](https://github.com/sgl-project/sglang/pull/35123) fix DSV4 FP4 dequant path for AITER on ROCm
- [#35455](https://github.com/sgl-project/sglang/pull/35455) load compressed-tensors kv_cache_scheme scales
</details>

<details>
<summary>Model support (20)</summary>

- [#34980](https://github.com/sgl-project/sglang/pull/34980) native Hunyuan3D Paint and Delight models
- [#35006](https://github.com/sgl-project/sglang/pull/35006) reuse SRT Qwen vision and text modules
- [#35370](https://github.com/sgl-project/sglang/pull/35370) load GGUF transformer checkpoints (MiniMax-H3)
- [#34896](https://github.com/sgl-project/sglang/pull/34896) use native Qwen2.5-VL generation
- [#34859](https://github.com/sgl-project/sglang/pull/34859) Qwen3.8-27B Model Support
- [#22498](https://github.com/sgl-project/sglang/pull/22498) add support for Gemma4 on Xeon
- [#34945](https://github.com/sgl-project/sglang/pull/34945) native Qwen3-VL vision encoder
- [#34988](https://github.com/sgl-project/sglang/pull/34988) reuse SRT SigLIP vision model
- [#34951](https://github.com/sgl-project/sglang/pull/34951) native ERNIE prompt enhancer
- [#35598](https://github.com/sgl-project/sglang/pull/35598) mirror support MiniMax H3 t2va rollout
- [#34992](https://github.com/sgl-project/sglang/pull/34992) reuse SRT SigLIP in Pi0.5
- [#35038](https://github.com/sgl-project/sglang/pull/35038) add native SenseNova U1 multimodal generation and interleave serving
- [#35314](https://github.com/sgl-project/sglang/pull/35314) support deepseek v4 and kimi k3 on ssd
- [#35014](https://github.com/sgl-project/sglang/pull/35014) support MAGI-2-preview
- [#35304](https://github.com/sgl-project/sglang/pull/35304) Intel XPU support for encoder embeddings (bge/NomicBERT/ModernBERT) + InternVL3_5
- [#35517](https://github.com/sgl-project/sglang/pull/35517) add Spark3 Model
- [#35599](https://github.com/sgl-project/sglang/pull/35599) support NemotronH_Omni_Reasoning_V3 in SGLang
- [#35532](https://github.com/sgl-project/sglang/pull/35532) add deepseek v3 bidirectional embedding
- [#35531](https://github.com/sgl-project/sglang/pull/35531) add qwen3 bidirectional embedding
- [#35418](https://github.com/sgl-project/sglang/pull/35418) support MiniMax-H3 pruned safetensors checkpoints
</details>

<details>
<summary>Parallelism & scheduling (53)</summary>

- [#34798](https://github.com/sgl-project/sglang/pull/34798) buffer-only mode for HiCache host memory layer
- [#34404](https://github.com/sgl-project/sglang/pull/34404) cache Kimi-K3 per-image processor artifacts
- [#35067](https://github.com/sgl-project/sglang/pull/35067) support L3 memcache and fix L2 cache issue on NPU
- [#34793](https://github.com/sgl-project/sglang/pull/34793) flatten L2 transfer execution in HiCache
- [#35269](https://github.com/sgl-project/sglang/pull/35269) support runtime attach/detach in UnifiedTree
- [#33480](https://github.com/sgl-project/sglang/pull/33480) support prefill context parallel two batch overlap for DeepSeek V4
- [#35049](https://github.com/sgl-project/sglang/pull/35049) deferred decode-side KV release for aborts mid-transfer
- [#34713](https://github.com/sgl-project/sglang/pull/34713) decouple encoder parallelism from DiT parallel layout
- [#34801](https://github.com/sgl-project/sglang/pull/34801) preserve decode KV across retraction in HiCache
- [#35360](https://github.com/sgl-project/sglang/pull/35360) deferred decode-side KV release for NIXL backend
- [#35543](https://github.com/sgl-project/sglang/pull/35543) allow a retraction host pool smaller than the device pool
- [#32313](https://github.com/sgl-project/sglang/pull/32313) optimize TP LMHead with All-to-All
- [#34998](https://github.com/sgl-project/sglang/pull/34998) add explicit EPLB balancedness reporting modes
- [#35248](https://github.com/sgl-project/sglang/pull/35248) discount queued prefill load by recent cache hits
- [#35071](https://github.com/sgl-project/sglang/pull/35071) overlap prefill DP-rank bootstrap queries
- [#35017](https://github.com/sgl-project/sglang/pull/35017) add configurable decode interval after prefill
- [#34519](https://github.com/sgl-project/sglang/pull/34519) limit load-back pending to write-back in HiCache
- [#34870](https://github.com/sgl-project/sglang/pull/34870) fix swa eviction frontier for bigram keys
- [#35540](https://github.com/sgl-project/sglang/pull/35540) split host-memory budget across co-located ranks
- [#35143](https://github.com/sgl-project/sglang/pull/35143) add bit-exact class for MTP
- [#33473](https://github.com/sgl-project/sglang/pull/33473) batch PP write and load completion sync
- [#34316](https://github.com/sgl-project/sglang/pull/34316) fix prefill FLOPs estimate to count prefix and per-request causal pairs
- [#35161](https://github.com/sgl-project/sglang/pull/35161) skip inkling sheared bias under batch invariance
- [#35070](https://github.com/sgl-project/sglang/pull/35070) avoid unused PREBUILT prompt tensor transfer
- [#33998](https://github.com/sgl-project/sglang/pull/33998) optimize LogicalHostPool free-list release
- [#35030](https://github.com/sgl-project/sglang/pull/35030) add bit-exact guard for extra_buffer_lazy
- [#35000](https://github.com/sgl-project/sglang/pull/35000) support unified SWA page mapping in attention metadata
- [#35191](https://github.com/sgl-project/sglang/pull/35191) cap prefill-delayer queue target by admission capacity
- [#35177](https://github.com/sgl-project/sglang/pull/35177) three sub-pools for mamba + hybrid-SWA models
- [#35426](https://github.com/sgl-project/sglang/pull/35426) deprecate Prefill CP V1
- [#35488](https://github.com/sgl-project/sglang/pull/35488) HiCache as the plugin logical KV pool
- [#35635](https://github.com/sgl-project/sglang/pull/35635) support partial-page prefix reuse in RadixCache
- [#35158](https://github.com/sgl-project/sglang/pull/35158) byte-budget sizing, feasibility floor, and a conservation verifier
- [#35637](https://github.com/sgl-project/sglang/pull/35637) improving Agentic RL Rollout Inference Efficiency with Uniboost Scheduler Policy
- [#35307](https://github.com/sgl-project/sglang/pull/35307) host pools and L3 namespacing for strict SWA offload on unified_kv + HiCache
- [#35435](https://github.com/sgl-project/sglang/pull/35435) add group-aware CPU SHM collective kernels
- [#35494](https://github.com/sgl-project/sglang/pull/35494) isolate C4 compress state per request for unified_kv
- [#35330](https://github.com/sgl-project/sglang/pull/35330) enable GB300 TP4 and GB200/GB300 TP16 SP collectives
- [#35281](https://github.com/sgl-project/sglang/pull/35281) align defensive protocol behavior across Mooncake, NIXL, and Mori
- [#35043](https://github.com/sgl-project/sglang/pull/35043) enable staged HiCache write-back for DeepSeek V4
- [#35641](https://github.com/sgl-project/sglang/pull/35641) plan pinned host memory against cgroup cap not machine
- [#35470](https://github.com/sgl-project/sglang/pull/35470) don't cache in-flight denoise block in radix tree
- [#35036](https://github.com/sgl-project/sglang/pull/35036) route equal-TP fragmented KV transfer through staging
- [#35132](https://github.com/sgl-project/sglang/pull/35132) enqueue middle prefill KV transfer after launch
- [#35515](https://github.com/sgl-project/sglang/pull/35515) SWA radix cache: evict branch tail sliding window last
- [#35093](https://github.com/sgl-project/sglang/pull/35093) propagate rank-local tensor update failures
- [#35157](https://github.com/sgl-project/sglang/pull/35157) hold non-stream forced intermediate output on a stop-string prefix
- [#35501](https://github.com/sgl-project/sglang/pull/35501) deduplicate shared SWA slots before free
- [#35040](https://github.com/sgl-project/sglang/pull/35040) use HIP batched copies for HiCache write-back
- [#35401](https://github.com/sgl-project/sglang/pull/35401) write req_to_token page tail so rows stay valid over whole pages
- [#35303](https://github.com/sgl-project/sglang/pull/35303) extension points for strict SWA state capture/restore on unified_kv + HiCache
- [#35009](https://github.com/sgl-project/sglang/pull/35009) scope write-back load-back pins by component
</details>

<details>
<summary>Speculative decoding (27)</summary>

- [#35371](https://github.com/sgl-project/sglang/pull/35371) DFlash2: local convolution + candidate selector
- [#35375](https://github.com/sgl-project/sglang/pull/35375) borrow CUDA graph pool storage for EAGLE sampling
- [#35024](https://github.com/sgl-project/sglang/pull/35024) size speculative buffers from bags, not startup record
- [#35496](https://github.com/sgl-project/sglang/pull/35496) support quantized target lm_head in DFlash2 selector
- [#35265](https://github.com/sgl-project/sglang/pull/35265) page-align DFLASH decode KV reservation
- [#35058](https://github.com/sgl-project/sglang/pull/35058) simplify compute_spec_v2_logprobs signature and skip identity gathers
- [#35382](https://github.com/sgl-project/sglang/pull/35382) share page-aligned decode alloc lens between EAGLE and DFLASH
- [#35059](https://github.com/sgl-project/sglang/pull/35059) resolve shared-read ends from backend declaration alone
- [#35198](https://github.com/sgl-project/sglang/pull/35198) relay ngram accept tokens through FutureMap
- [#34696](https://github.com/sgl-project/sglang/pull/34696) support logprobs with DSpark speculative decoding
- [#35195](https://github.com/sgl-project/sglang/pull/35195) scope EAGLE greedy-verify TP broadcast to ROCm only
- [#35102](https://github.com/sgl-project/sglang/pull/35102) support dynamic external ngram corpora
- [#35413](https://github.com/sgl-project/sglang/pull/35413) derive DSpark verify-budget cost table at CUDA graph capture
- [#35577](https://github.com/sgl-project/sglang/pull/35577) add Mooncake GPU-direct SpecForge capture
- [#35670](https://github.com/sgl-project/sglang/pull/35670) support DSpark compact verify graph and folded verify epilogue
- [#35629](https://github.com/sgl-project/sglang/pull/35629) adapt DFlash2 speculative decoding to Ascend NPUs
- [#35624](https://github.com/sgl-project/sglang/pull/35624) bound DSpark rejection sampling workspace
- [#35544](https://github.com/sgl-project/sglang/pull/35544) amortize ReplaySSM checkpoint materialization
- [#35300](https://github.com/sgl-project/sglang/pull/35300) enable target-only mixed chunked prefill for DSpark
- [#35566](https://github.com/sgl-project/sglang/pull/35566) account native Qwen3.5/3.8 MTP KV layers in target pool sizing
- [#35580](https://github.com/sgl-project/sglang/pull/35580) fail loudly when DFlash2 selector top_k exceeds org vocab
- [#35581](https://github.com/sgl-project/sglang/pull/35581) resolve DFlash2 selector shard metadata once for both TP modes
- [#35583](https://github.com/sgl-project/sglang/pull/35583) allow independent draft model config overrides
- [#35588](https://github.com/sgl-project/sglang/pull/35588) fix full prefill CUDA graph padding and EAGLE capture
- [#35321](https://github.com/sgl-project/sglang/pull/35321) support dp attention for DFLASH speculative decoding
- [#35126](https://github.com/sgl-project/sglang/pull/35126) stage EAGLE draft-extend graph inputs before verify launch
- [#35275](https://github.com/sgl-project/sglang/pull/35275) fix startup crash and reduce CUDA graph memory usage for speculative adaptive
</details>

<details>
<summary>Hardware & arch (7)</summary>

- [#35432](https://github.com/sgl-project/sglang/pull/35432) support 950 glm cache service on NPU
- [#35569](https://github.com/sgl-project/sglang/pull/35569) NPU support o tp
- [#35237](https://github.com/sgl-project/sglang/pull/35237) add SM100 NVFP4 KV cache support for GLM-5.2 DSA
- [#35048](https://github.com/sgl-project/sglang/pull/35048) account for reserved hugepages in HiCache host memory check
- [#35186](https://github.com/sgl-project/sglang/pull/35186) stage MLA DCP=8 relayout before Mooncake RDMA for KIMI K3
- [#35072](https://github.com/sgl-project/sglang/pull/35072) support prefill only models for Intel XPU
- [#35451](https://github.com/sgl-project/sglang/pull/35451) support PP in full prefill CUDA graphs
</details>

<details>
<summary>API & serving (21)</summary>

- [#35339](https://github.com/sgl-project/sglang/pull/35339) per-request lossy accelerations: Cache-DiT, CFG gating, attention backend override
- [#33518](https://github.com/sgl-project/sglang/pull/33518) add sglext_spec to API
- [#35550](https://github.com/sgl-project/sglang/pull/35550) add --default-top-k / --default-top-p to set fleet-wide sampling defaults
- [#35215](https://github.com/sgl-project/sglang/pull/35215) support MistralCommon tokenizers in XGrammar backend
- [#33606](https://github.com/sgl-project/sglang/pull/33606) accept input_audio content part in chat completions
- [#35001](https://github.com/sgl-project/sglang/pull/35001) apply request header overrides to chat completions
- [#35261](https://github.com/sgl-project/sglang/pull/35261) add key_id + ingest prompt_len to S3 token export
- [#35205](https://github.com/sgl-project/sglang/pull/35205) make sampling-support capture faithful and capacity-safe
- [#35166](https://github.com/sgl-project/sglang/pull/35166) publish gRPC breaker outcomes at selected body terminal
- [#35216](https://github.com/sgl-project/sglang/pull/35216) Responses API Codex compatibility: custom tools, namespace tools, agent_message, array tool output
- [#35613](https://github.com/sgl-project/sglang/pull/35613) scope model-specific API parameters for diffusion
- [#35325](https://github.com/sgl-project/sglang/pull/35325) add video input support for Kimi-K3
- [#35069](https://github.com/sgl-project/sglang/pull/35069) decompose pre-first-token path into phase histograms
- [#35516](https://github.com/sgl-project/sglang/pull/35516) extract OpenAI request preparation from inference handlers
- [#35352](https://github.com/sgl-project/sglang/pull/35352) ComfyUI: add MiniMax-H3 node and generic extra-fields passthrough
- [#35262](https://github.com/sgl-project/sglang/pull/35262) accept token ID prompts in /v1/completions
- [#35235](https://github.com/sgl-project/sglang/pull/35235) add `--insecure` to skip TLS verification
- [#35625](https://github.com/sgl-project/sglang/pull/35625) make streaming tool-call parsing agree with non-streaming
- [#35475](https://github.com/sgl-project/sglang/pull/35475) add unit tests for FunctionCallParser and BaseFormatDetector
- [#35169](https://github.com/sgl-project/sglang/pull/35169) keep normal text preceding tool-call opener in streaming parsers
- [#35081](https://github.com/sgl-project/sglang/pull/35081) using unified radix tree by default for all case
- [#35651](https://github.com/sgl-project/sglang/pull/35651) tighten multimodal media trust boundaries
</details>

<details>
<summary>Tests, CI & build (30)</summary>

- [#35511](https://github.com/sgl-project/sglang/pull/35511) CI: add minimax-h3 ref2va audio consistency coverage and guard peak vram
- [#35407](https://github.com/sgl-project/sglang/pull/35407) trim base-c 4-gpu-h100 stage from 5 shards to 4
- [#33685](https://github.com/sgl-project/sglang/pull/33685) reorganize test output/log directory structure with workflow context
- [#34994](https://github.com/sgl-project/sglang/pull/34994) build Rust extensions on demand in source checkouts
- [#35044](https://github.com/sgl-project/sglang/pull/35044) stabilize GB300 nightly tests
- [#30984](https://github.com/sgl-project/sglang/pull/30984) upgrade Python 3.12 + torch 2.11 + triton 3.7 in ROCm 7.2.4
- [#35502](https://github.com/sgl-project/sglang/pull/35502) add three new test cases
- [#35603](https://github.com/sgl-project/sglang/pull/35603) run Both ROCm 7.2.4 and ROCm 7.2.0 Images on Nightly Test AMD
- [#34645](https://github.com/sgl-project/sglang/pull/34645) add GPT-OSS perf benchmarks to ROCm 7.2 nightly
- [#32570](https://github.com/sgl-project/sglang/pull/32570) add GLM-5.2 MI35x nightly accuracy and perf benchmark
- [#34984](https://github.com/sgl-project/sglang/pull/34984) make Kimi-K3 MI35x nightly accuracy-only, and fix lint blocker
- [#32568](https://github.com/sgl-project/sglang/pull/32568) add Kimi-K3 8-GPU MI35x nightly accuracy CI
- [#33679](https://github.com/sgl-project/sglang/pull/33679) XPU kernel release workflow
- [#34985](https://github.com/sgl-project/sglang/pull/34985) add Kimi-K3 MI35x perf benchmarks in nightly
- [#35337](https://github.com/sgl-project/sglang/pull/35337) key persistent JIT kernel cache by image content ID
- [#34813](https://github.com/sgl-project/sglang/pull/34813) surface AMD ROCm 7.2 state in PR CI-states block
- [#30612](https://github.com/sgl-project/sglang/pull/30612) install sglang in virtual env instead of system path
- plus 13 more minor CI updates
</details>

<details>
<summary>Docs (13)</summary>

- [#35065](https://github.com/sgl-project/sglang/pull/35065) Qwen3.8-27B deployment grid rework
- [#35597](https://github.com/sgl-project/sglang/pull/35597) add a comment style rule to .claude/rules
- [#35436](https://github.com/sgl-project/sglang/pull/35436) add a fused-kernels page for SGLang Diffusion
- [#35419](https://github.com/sgl-project/sglang/pull/35419) update contribution guide
- [#35121](https://github.com/sgl-project/sglang/pull/35121) add Qwen3.8-27B DGX Spark configs
- [#35218](https://github.com/sgl-project/sglang/pull/35218) sync LMSYS SGLang blog cards
- [#35458](https://github.com/sgl-project/sglang/pull/35458) PaddleOCR-VL: say which stage of pipeline this serves, show real output
- [#35168](https://github.com/sgl-project/sglang/pull/35168) add NVFP4 quantization option to Kimi-K3 deploy panel
- [#35224](https://github.com/sgl-project/sglang/pull/35224) enable PD disaggregation for DSV4 low-latency recipes
- [#35679](https://github.com/sgl-project/sglang/pull/35679) refresh eager optimization skills and benchmark safeguards
- [#35508](https://github.com/sgl-project/sglang/pull/35508) add Ascend NPU (A3) recipe to Kimi-K3 cookbook
- [#35468](https://github.com/sgl-project/sglang/pull/35468) add ComfyUI section for every diffusion cookbook page
- [#35622](https://github.com/sgl-project/sglang/pull/35622) trim restating comments and docstrings in srt/managers
</details>

<details>
<summary>Bugfixes (36)</summary>

- [#32611](https://github.com/sgl-project/sglang/pull/32611) fix transcription & audio-understanding for ASR/audio/speech models
- [#34663](https://github.com/sgl-project/sglang/pull/34663) refresh docs, retire stale knobs, and fix nightly attribution
- [#31575](https://github.com/sgl-project/sglang/pull/31575) fix rope config compatibility and VL/transformers-fallback weight loading
- [#35182](https://github.com/sgl-project/sglang/pull/35182) reject unsupported modelopt checkpoint algorithms
- [#34993](https://github.com/sgl-project/sglang/pull/34993) make MiniMax-H3 AdaLN cache rebuild transactional
- [#35125](https://github.com/sgl-project/sglang/pull/35125) add e2e latency metadata and fix Sarashina import
- [#35626](https://github.com/sgl-project/sglang/pull/35626) keep large vocab tables in host memory under layerwise offload
- [#35184](https://github.com/sgl-project/sglang/pull/35184) route quantized VAE component repos safely
- [#12961](https://github.com/sgl-project/sglang/pull/12961) fix DP attention on CPU
- [#35509](https://github.com/sgl-project/sglang/pull/35509) fix multi-group layerwise offload startup memory
- [#34679](https://github.com/sgl-project/sglang/pull/34679) reject NUL bytes in grammar specs to stop xgrammar segfault
- [#35576](https://github.com/sgl-project/sglang/pull/35576) cherry-pick [#34679](https://github.com/sgl-project/sglang/pull/34679)
- [#35130](https://github.com/sgl-project/sglang/pull/35130) fix NIXL cleaner grouping for hybrid cache keys
- [#35064](https://github.com/sgl-project/sglang/pull/35064) fix Qwen3.8-27B mamba ratio calculator for speculative decoding
- [#35538](https://github.com/sgl-project/sglang/pull/35538) stop reserving NCCL device buffers for single-rank groups
- [#34485](https://github.com/sgl-project/sglang/pull/34485) let diffusion AITer backend take grouped-query K/V
- [#35298](https://github.com/sgl-project/sglang/pull/35298) DCP: advertise logical KV-event block size
- [#35590](https://github.com/sgl-project/sglang/pull/35590) cherry-pick [#35298](https://github.com/sgl-project/sglang/pull/35298)
- [#34627](https://github.com/sgl-project/sglang/pull/34627) preserve output logprobs without input logprobs
- [#34481](https://github.com/sgl-project/sglang/pull/34481) keep PTX-inline-asm diffusion norm fusions off on ROCm
- [#33431](https://github.com/sgl-project/sglang/pull/33431) skip padded state slots in chunked GDN kernel
- [#35589](https://github.com/sgl-project/sglang/pull/35589) bug fix pp + pd
- [#35013](https://github.com/sgl-project/sglang/pull/35013) split packed MTP HiCache transfers by pool
- [#35154](https://github.com/sgl-project/sglang/pull/35154) four boot/correctness fixes on hybrid model paths
- [#35115](https://github.com/sgl-project/sglang/pull/35115) stop freezing scheduler thread while chrome trace is written
- [#35606](https://github.com/sgl-project/sglang/pull/35606) fix mambacache & fused ops on NPU
- [#35393](https://github.com/sgl-project/sglang/pull/35393) stop unparsed Kimi K3 template syntax from leaking into responses
- [#35233](https://github.com/sgl-project/sglang/pull/35233) fix registered HiCache host pointer aliases
- [#35592](https://github.com/sgl-project/sglang/pull/35592) decide SWA slot liveness on host instead of device-side mask
- [#35217](https://github.com/sgl-project/sglang/pull/35217) chunk DSV4 indexer logits to bound transient memory
- [#35008](https://github.com/sgl-project/sglang/pull/35008) fix Qwen3 Coder stalls on large string tool arguments
- [#35051](https://github.com/sgl-project/sglang/pull/35051) pack device-pointer tables as uint64 to avoid 64-bit address overflow
- [#35255](https://github.com/sgl-project/sglang/pull/35255) abort handling for dispatched requests after client disconnect
- [#35090](https://github.com/sgl-project/sglang/pull/35090) use monotonic_time() for received_time to fix negative Prometheus metrics
- [#35153](https://github.com/sgl-project/sglang/pull/35153) DeepSeek-V3.1 streaming tool-call detector loses calls at chunk boundaries
- [#35136](https://github.com/sgl-project/sglang/pull/35136) fix TeaCache CFG state lifecycle
- [#35140](https://github.com/sgl-project/sglang/pull/35140) fix Spectrum state reset for CFG-parallel branches
- [#35152](https://github.com/sgl-project/sglang/pull/35152) skip redundant routed_scaling_factor in TBO DeepseekV2MoE.op_output
- [#35312](https://github.com/sgl-project/sglang/pull/35312) fix p2p weight registry: draft worker overwrite, fused indexer mapping, registration retries
</details>

<details>
<summary>Refactors (13)</summary>

- [#34736](https://github.com/sgl-project/sglang/pull/34736) unify component residency controls
- [#31180](https://github.com/sgl-project/sglang/pull/31180) move MambaPoolHost to pool_host.mamba
- [#35060](https://github.com/sgl-project/sglang/pull/35060) clean up environ.py: remove dead env vars, unify deprecation handling
- [#35164](https://github.com/sgl-project/sglang/pull/35164) refactor kv cache event mixin into a recorder
- [#35183](https://github.com/sgl-project/sglang/pull/35183) gate native encoder quantized checkpoints
- [#31453](https://github.com/sgl-project/sglang/pull/31453) refactor and extract complex RoPE implementation to layers/rotary_embedding for MOVA DiT
- [#34982](https://github.com/sgl-project/sglang/pull/34982) rename shared-read boundary to shared-read ends and fix wrapper delegation
- [#35621](https://github.com/sgl-project/sglang/pull/35621) root JIT kernel cache under SGLANG_CACHE_DIR
- [#35247](https://github.com/sgl-project/sglang/pull/35247) route KV read path through one id-space choke point
- [#35245](https://github.com/sgl-project/sglang/pull/35245) translate KV write location once, at ForwardBatch construction
- [#35638](https://github.com/sgl-project/sglang/pull/35638) ratchet allocator and pool_host layout
- [#35306](https://github.com/sgl-project/sglang/pull/35306) move DSAIndexerPoolHost to pool_host.dsa
- [#35647](https://github.com/sgl-project/sglang/pull/35647) extract KVCache and BaseSWAKVPool into pool/base.py
</details>

<details>
<summary>Other (37)</summary>

- [#35026](https://github.com/sgl-project/sglang/pull/35026) config: per-instance families read bags
- [#35027](https://github.com/sgl-project/sglang/pull/35027) config: readback and resolving view say what they are
- [#34926](https://github.com/sgl-project/sglang/pull/34926) clean deprecated DeepSeek V4 Environs
- [#35025](https://github.com/sgl-project/sglang/pull/35025) config: DP/EP topology reads come from parallel bag
- [#35062](https://github.com/sgl-project/sglang/pull/35062) clean up python/sglang package structure
- [#24911](https://github.com/sgl-project/sglang/pull/24911) Profiling Enhancements [2/3]: detailed execution step annotations
- [#35023](https://github.com/sgl-project/sglang/pull/35023) config: publish before a process reads configuration
- [#35022](https://github.com/sgl-project/sglang/pull/35022) config: retire multi-engine accommodation in runtime context
- [#34881](https://github.com/sgl-project/sglang/pull/34881) stop losing Kimi-K3 tool calls to reasoning, constraint conflicts, and truncation
- [#35399](https://github.com/sgl-project/sglang/pull/35399) cherry-pick [#34881](https://github.com/sgl-project/sglang/pull/34881)
- [#35018](https://github.com/sgl-project/sglang/pull/35018) clean up playground scripts and add PR babysitter launcher
- [#35028](https://github.com/sgl-project/sglang/pull/35028) config: one control-plane log for process
- [#34197](https://github.com/sgl-project/sglang/pull/34197) RL rollout support for Cosmos3 pipeline
- [#34995](https://github.com/sgl-project/sglang/pull/34995) avoid synchronizing multimodal placeholder counts
- [#35575](https://github.com/sgl-project/sglang/pull/35575) make PR babysitter launcher fork-safe
- [#35034](https://github.com/sgl-project/sglang/pull/35034) add preprocess-cache observability and agentic benchmark coverage
- [#35239](https://github.com/sgl-project/sglang/pull/35239) rainj me/rust server refactor2
- [#35033](https://github.com/sgl-project/sglang/pull/35033) reuse Kimi-K3 embeddings before encoder preprocessing
- [#35127](https://github.com/sgl-project/sglang/pull/35127) extract Anthropic conversion into standalone utils
- [#35259](https://github.com/sgl-project/sglang/pull/35259) harden startup weight-load overlap and expand model coverage
- [#35344](https://github.com/sgl-project/sglang/pull/35344) step-reuse execution contract for iterative denoising models
- [#35359](https://github.com/sgl-project/sglang/pull/35359) compile-plan trajectory promotion gate
- [#35350](https://github.com/sgl-project/sglang/pull/35350) candidate-trajectory execution contract
- [#35618](https://github.com/sgl-project/sglang/pull/35618) UX: report where a component's weights are
- [#35664](https://github.com/sgl-project/sglang/pull/35664) warn on unverified short edge instead of rejecting it for minimax-h3
- [#35320](https://github.com/sgl-project/sglang/pull/35320) lmhead tp
- [#35266](https://github.com/sgl-project/sglang/pull/35266) K3
- [#35678](https://github.com/sgl-project/sglang/pull/35678) Pcp rebase
- [#35463](https://github.com/sgl-project/sglang/pull/35463) split Pixtral multi-image features before CUDA IPC wrap
- [#35326](https://github.com/sgl-project/sglang/pull/35326) add ProductionDebtRadixCacheGate and TechnicalDueDiligenceLedger
- [#35311](https://github.com/sgl-project/sglang/pull/35311) add ProductionDebtInferenceGate and TechnicalDueDiligenceLedger
- [#35668](https://github.com/sgl-project/sglang/pull/35668) make weight source a reader, not a boolean
- [#35349](https://github.com/sgl-project/sglang/pull/35349) default to two multimodal preprocessing workers
- [#35342](https://github.com/sgl-project/sglang/pull/35342) route every multimodal processor through worker pool's call site
- [#35343](https://github.com/sgl-project/sglang/pull/35343) sync FlashInfer autotune tactic choice across TP ranks
- [#35346](https://github.com/sgl-project/sglang/pull/35346) initialize reasoning parser from prefilled think token
- [#35680](https://github.com/sgl-project/sglang/pull/35680) add Vast.ai dev-install script for PP activation-compression research
- [#35395](https://github.com/sgl-project/sglang/pull/35395) only open MTP-head shards for NextN/MTP draft load
- [#35567](https://github.com/sgl-project/sglang/pull/35567) bind native Qwen MTP embed/lm_head before memory pool allocation
</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (sglang.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 313245c7a4f574511937fad9af32d41afe4cbf37dcdd46cd2ac6e7c8767b883c -->
