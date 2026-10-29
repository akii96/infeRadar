# AITER: PR digest (2026-10-25 to 2026-10-29)

_152 merged, 166 newly opened - source ROCm/AITER, generated 2026-10-29T15:59:27Z_

## TL;DR
- **Model focus:** DeepSeek (V4/V4.1), Kimi (K2/K3, KDA), and Qwen (3.5/3.8) got the most attention, followed by GLM-5.3 and MiniMax-M3. Most of the work was tuned GEMM and MoE configs plus new quantized kernels.
- **gfx1250 is the main arch push:** Gluon and FlyDSL GEMM tuning for DSR1, Kimi-K2 and Qwen3.5; new FP8/BF8 FMHA; MXFP4 a4w4 GEMM; grouped MoE A-preshuffle; fused all-reduce+RMSNorm. gfx950 got MXFP8/MXFP6 GEMM, MLA v4.1 prefill and flash-KDA work.
- **Attention and MLA:** a gfx950 MLA v4.1 sparse prefill with split-K, an MHA v4 refresh, and gfx950/gfx1250 Gluon MHA and KDA kernels. Open PRs add FP4/MXFP4 KV and index caches and a gfx942 FP4 paged MQA.
- **Overall direction:** low-precision quantization (MXFP4/MXFP8/NVFP4) across GEMM, MoE and attention. Correctness fixes (races, `num_local_tokens` bounds, custom all-reduce) and host-overhead cuts ride along. CI is shifting toward diff-selected tests.

## Most important PRs
**[#6675](https://github.com/ROCm/aiter/pull/6675) gfx950 MLA v4.1 and split-K for the OPUS sparse MLA prefill**
Adds a v4.1 sparse-MLA prefill path with split-K on gfx950 and moves the dispatch to ctypes. It is the core DeepSeek-style prefill kernel work. [#7036](https://github.com/ROCm/aiter/pull/7036) adds a 16mx1 prefill kernel for H ≤ 16 on top of it.

**[#6702](https://github.com/ROCm/aiter/pull/6702) FlyDSL FMHA FP8/BF8 on gfx1250**
Adds FP8/BF8 support to the gfx1250 FMHA. This is a main building block for low-precision prefill on the new arch.

**[#6362](https://github.com/ROCm/aiter/pull/6362) Build MoE and MegaMoE AOT caches by replaying the runtime on CPU**
Precompiles FlyDSL MoE kernels without a GPU, which cuts serving-time JIT cost and cold-start recompiles. Open [#7063](https://github.com/ROCm/aiter/pull/7063) and [#6956](https://github.com/ROCm/aiter/pull/6956) extend the approach to EP/TP deployments, GEMM, conv and FMHA.

**[#6621](https://github.com/ROCm/aiter/pull/6621) gfx1250 MXFP4 a4w4 GEMM with tuned DSR1 configs**
A new FlyDSL MXFP4 GEMM for gfx1250 shipped with DeepSeek-R1 tuning. [#6913](https://github.com/ROCm/aiter/pull/6913) and [#7038](https://github.com/ROCm/aiter/pull/7038) add matching Gluon and MXFP8 tunings for DSR1, MiniMax-M3 and DSV4.1.

**[#6614](https://github.com/ROCm/aiter/pull/6614) Fused dvdk and dq with split-K, pingpong pipeline**
Fuses the dK/dV and dQ attention backward passes with split-K and a pingpong pipeline, which cuts backward-attention launches and memory traffic.

## More changes by area

<details>
<summary>Performance (10)</summary>

- [#6946](https://github.com/ROCm/aiter/pull/6946) cache compiled FlyDSL launchers on host paths
- [#7006](https://github.com/ROCm/aiter/pull/7006) cut remaining host overhead in FlyDSL GEMM/MoE wrappers on gfx1250
- [#6762](https://github.com/ROCm/aiter/pull/6762) cache per-config host work on the FlyDSL GEMM launch path
- [#6984](https://github.com/ROCm/aiter/pull/6984) optimize gfx1250 MoE A-preshuffle preparation and prefill scheduling
- [#5973](https://github.com/ROCm/aiter/pull/5973) optimize MI308 MoE decoding
- [#6943](https://github.com/ROCm/aiter/pull/6943) optimize gfx1250 BF16 page16 and FP8 attention
- [#6668](https://github.com/ROCm/aiter/pull/6668) MiniMax-M3 MoE on gfx1250: fused route psum and tuned A8W4 tiles
- [#5921](https://github.com/ROCm/aiter/pull/5921) derive the fp8_mqa_logits split target from kernel occupancy
- [#6001](https://github.com/ROCm/aiter/pull/6001) drop host row-pad copies in fp8_mqa_logits
- [#5925](https://github.com/ROCm/aiter/pull/5925) stop serving-time recompiles of _prefill_row_plan_kernel

</details>

<details>
<summary>Kernels & attention (24)</summary>

- [#6937](https://github.com/ROCm/aiter/pull/6937) OPUS global kid to local kid
- [#6988](https://github.com/ROCm/aiter/pull/6988) hybrid pinning and ASIC-aware gfx1250 A0 code objects
- [#7014](https://github.com/ROCm/aiter/pull/7014) reland topk per row on gfx950 (without topk_plain on gfx1250)
- [#5686](https://github.com/ROCm/aiter/pull/5686) topk per row on gfx950 (FlyDSL)
- [#6991](https://github.com/ROCm/aiter/pull/6991) revert of [#5686](https://github.com/ROCm/aiter/pull/5686)
- [#5153](https://github.com/ROCm/aiter/pull/5153) productize Gluon MHA on gfx950
- [#6609](https://github.com/ROCm/aiter/pull/6609) gfx1250 flash KDA Gluon
- [#6177](https://github.com/ROCm/aiter/pull/6177) faster FlashKDA and token-parallel intra forward on gfx950
- [#7045](https://github.com/ROCm/aiter/pull/7045) MHA MXFP8 subtiled kernel
- [#6508](https://github.com/ROCm/aiter/pull/6508) MHA FP8 subtiled kernel
- [#6841](https://github.com/ROCm/aiter/pull/6841) MHA v4: LSE on sorted-sparse, race fixes, gfx950 refresh
- [#6815](https://github.com/ROCm/aiter/pull/6815) opt-in prefix-budget metadata planner for PA
- [#6515](https://github.com/ROCm/aiter/pull/6515) QSA paged MQA logits MFMA scorer for prefill
- [#6450](https://github.com/ROCm/aiter/pull/6450) read (B, next_n) context lengths in the paged MQA logits kernel
- [#5977](https://github.com/ROCm/aiter/pull/5977) asm MHA bf16 hd192x128 with strided q/k/v/out
- [#6897](https://github.com/ROCm/aiter/pull/6897) FMHA prefill v_hdim 256 on gfx1250
- [#7087](https://github.com/ROCm/aiter/pull/7087) mla_reduce_v1 with 12 heads at head dim 128
- [#7112](https://github.com/ROCm/aiter/pull/7112) fused GDN speculative-verify step on ReplaySSM state
- [#6896](https://github.com/ROCm/aiter/pull/6896) unified_attention spec-decode verify on gfx1250
- [#7115](https://github.com/ROCm/aiter/pull/7115) split-K tuning for mhc_fused_post_pre_delayed_rmsnorm decode
- [#3269](https://github.com/ROCm/aiter/pull/3269) block_cat_fused op
- [#6845](https://github.com/ROCm/aiter/pull/6845) padding-mode support for routed Triton Conv2D
- [#7026](https://github.com/ROCm/aiter/pull/7026) expose paged backend arch support
- [#7113](https://github.com/ROCm/aiter/pull/7113) register-resident top-p sampling on gfx1250

</details>

<details>
<summary>MoE & quantization (24)</summary>

- [#6461](https://github.com/ROCm/aiter/pull/6461) staged search for the MXFP4 MoE tuner
- [#6527](https://github.com/ROCm/aiter/pull/6527) AITER_FLYDSL_USE_HERD on gfx1250 with a fused HERD selector for GPT-OSS
- [#6709](https://github.com/ROCm/aiter/pull/6709) gfx1250 grouped MoE A-preshuffle and tuned CSV validation
- [#6060](https://github.com/ROCm/aiter/pull/6060) gfx950 MXFP8 bmm with 1x32 weight scales and MiniMax-M3 configs
- [#6864](https://github.com/ROCm/aiter/pull/6864) batched mxfp8_32 GEMM with 32x32 weight scales on gfx1250
- [#6437](https://github.com/ROCm/aiter/pull/6437) gemm_a8w8_bpreshuffle_out for caller-owned bf16 outputs
- [#6736](https://github.com/ROCm/aiter/pull/6736) K=128 for gfx950 fp8 stage2 when 256 does not divide inter_dim
- [#7095](https://github.com/ROCm/aiter/pull/7095) gfx1250 TP MoE route histograms for wide expert sets
- [#7004](https://github.com/ROCm/aiter/pull/7004) handle -1 pad-row routes in the gfx1250 TP grouped MoE
- [#7067](https://github.com/ROCm/aiter/pull/7067) register top-k for E % 4 and mixed-dtype bias, plus a16w4 stage2 reduce mode
- [#6916](https://github.com/ROCm/aiter/pull/6916) pad-row routing count, custom all_gatherv, MoE quant-sort race fix
- [#6938](https://github.com/ROCm/aiter/pull/6938) pad-row count for HERD, gfx1250 sigmoid top-k, MXFP4 sort+quant
- [#7020](https://github.com/ROCm/aiter/pull/7020) MXFP4 inline-sort accepts num_local_tokens
- [#7085](https://github.com/ROCm/aiter/pull/7085) keep MX quant-sort and multi-phase sort in bounds under num_local_tokens
- [#6519](https://github.com/ROCm/aiter/pull/6519) bound scatter-reduce staging reads
- [#6677](https://github.com/ROCm/aiter/pull/6677) bound per-tensor quant vector tails
- [#6934](https://github.com/ROCm/aiter/pull/6934) honour row-strided output in a8w8 blockscale bpreshuffle GEMM
- [#6825](https://github.com/ROCm/aiter/pull/6825) gfx950 MXFP6 GEMM tuning candidates
- [#6049](https://github.com/ROCm/aiter/pull/6049) QuickAllReduce INT4 shared global divisor to avoid E4M3 scale saturation
- [#6404](https://github.com/ROCm/aiter/pull/6404) hidden 6144 in the INT4 QuickReduce + RMSNorm epilogue
- [#3813](https://github.com/ROCm/aiter/pull/3813) simplify ck_gemm_a8w8_blockscale GemmSpecialization
- [#7016](https://github.com/ROCm/aiter/pull/7016) preserve typed E8M0 scales in gfx1250 MoE routing
- [#6966](https://github.com/ROCm/aiter/pull/6966) skip redundant MORI counter reset
- [#6782](https://github.com/ROCm/aiter/pull/6782) is_sw_emulated_fp8_avail for gfx11, enabling the Triton MHA fp8 path

</details>

<details>
<summary>Tuning configs by model (34)</summary>

- [#6913](https://github.com/ROCm/aiter/pull/6913) gfx1250 Gluon GEMMs for DeepSeek-R1 TP4
- [#6573](https://github.com/ROCm/aiter/pull/6573) Kimi-K2 TP8 Gluon GEMM
- [#6903](https://github.com/ROCm/aiter/pull/6903) Kimi-K2 Thinking TP4 Gluon GEMM
- [#6901](https://github.com/ROCm/aiter/pull/6901) Qwen3.5-35B-A3B TP4 Gluon GEMM
- [#6910](https://github.com/ROCm/aiter/pull/6910) Qwen3.5-35B-A3B TP1 Gluon GEMM
- [#6870](https://github.com/ROCm/aiter/pull/6870) GPT-OSS 120B TP4 a16w16
- [#6871](https://github.com/ROCm/aiter/pull/6871) Llama3 8B MXFP4 TP4 Gluon
- [#6872](https://github.com/ROCm/aiter/pull/6872) Llama3 70B MXFP4 TP4 Gluon
- [#6873](https://github.com/ROCm/aiter/pull/6873) Llama3 405B MXFP4 TP4 Gluon
- [#6921](https://github.com/ROCm/aiter/pull/6921) use the M_LEQ_8192 config as "any" in tuned gfx1250 Gluon GEMM files
- [#7105](https://github.com/ROCm/aiter/pull/7105) configs per CU count (<arch>/<cu_num>cu trees)
- [#6771](https://github.com/ROCm/aiter/pull/6771) gfx1100 A16W16 for Llama-3-8B and Qwen3 shapes
- [#6530](https://github.com/ROCm/aiter/pull/6530) Kimi-K3 gfx1250 mxfp8_128 blockscale
- [#6763](https://github.com/ROCm/aiter/pull/6763) Kimi-K3 TP8 gfx1250 gemm
- [#6768](https://github.com/ROCm/aiter/pull/6768) Kimi-K3 TP8 gfx1250 grouped MoE
- [#7070](https://github.com/ROCm/aiter/pull/7070) Kimi-K2 TP8 gfx1250 FlyDSL bf16 rows
- [#6410](https://github.com/ROCm/aiter/pull/6410) Kimi-K3 gfx950 A8W8 bpreshuffle
- [#6820](https://github.com/ROCm/aiter/pull/6820) Kimi-K3 gfx950 BF16 MoE-front and DSpark draft QKV rows
- [#6711](https://github.com/ROCm/aiter/pull/6711) Qwen3.8-Flash-Next BF16 GEMMs on gfx950
- [#6713](https://github.com/ROCm/aiter/pull/6713) Qwen3.8-Flash-Next PTPC a8w8 bpreshuffle
- [#6708](https://github.com/ROCm/aiter/pull/6708) Qwen3.8-Flash-Next MXFP4 a4w4 MoE
- [#6025](https://github.com/ROCm/aiter/pull/6025) Qwen3.8 mxfp4 con 32/64 with emsort asm
- [#6898](https://github.com/ROCm/aiter/pull/6898) ASM split-K rows for Qwen3-14B-FP8
- [#6939](https://github.com/ROCm/aiter/pull/6939) MI350P Qwen38-27B-FP8 blockscale
- [#5999](https://github.com/ROCm/aiter/pull/5999) qwen35 bf16 GEMM on gfx1250
- [#6535](https://github.com/ROCm/aiter/pull/6535) MI300A GLM-5.3 FP8 blockscale GEMM and MoE
- [#6435](https://github.com/ROCm/aiter/pull/6435) GLM-5.3-Flash MXFP4 fused-MoE on MI355X
- [#6942](https://github.com/ROCm/aiter/pull/6942) MiniMax-M3.1 MXFP4 MoE (E=128 top-4)
- [#6936](https://github.com/ROCm/aiter/pull/6936) DeepSeek-V4.1 MXFP8 32x32 tiles on gfx1250
- [#7068](https://github.com/ROCm/aiter/pull/7068) DeepSeek-V4.1 MegaMoE grouped MoE on gfx1250
- [#6928](https://github.com/ROCm/aiter/pull/6928) retune DSV4 EP8 a8w4 fused-MoE rows
- [#5821](https://github.com/ROCm/aiter/pull/5821) DeepSeek-V4 EP8 a8w4 MXFP4 rows
- [#6977](https://github.com/ROCm/aiter/pull/6977) DSR1 FP4 MoE router GEMM
- [#6286](https://github.com/ROCm/aiter/pull/6286) retune gfx942 a16w4 DSv4.1 tiles for Triton 3.8
- plus [#6817](https://github.com/ROCm/aiter/pull/6817), [#6953](https://github.com/ROCm/aiter/pull/6953), [#6980](https://github.com/ROCm/aiter/pull/6980), [#7038](https://github.com/ROCm/aiter/pull/7038) and [#7018](https://github.com/ROCm/aiter/pull/7018)-style small config additions (gfx1151/gfx1150 and Muse Spark rows)

</details>

<details>
<summary>Parallelism & scheduling (9)</summary>

- [#6923](https://github.com/ROCm/aiter/pull/6923) gfx1250 Gluon all-reduce for 4 ranks
- [#6924](https://github.com/ROCm/aiter/pull/6924) gfx1250 Gluon fused all-reduce + residual + RMSNorm + fp8 group quant
- [#6974](https://github.com/ROCm/aiter/pull/6974) use the gfx1250 Gluon fused all-reduce + RMSNorm in fused_allreduce_rmsnorm
- [#6699](https://github.com/ROCm/aiter/pull/6699) fix gfx1250 fused all-reduce + RMSNorm in custom-ar
- [#6954](https://github.com/ROCm/aiter/pull/6954) sum ranks in a fixed order on every custom_ar reduce path
- [#6819](https://github.com/ROCm/aiter/pull/6819) keep CUDA-graph buffer registration in step across ranks
- [#5775](https://github.com/ROCm/aiter/pull/5775) send the real IPC offset in custom all-reduce
- [#6618](https://github.com/ROCm/aiter/pull/6618) manage v2 CCO through the all2all manager
- [#5182](https://github.com/ROCm/aiter/pull/5182) identify MI350P and stop hardcoding the XCD count

</details>

<details>
<summary>Bugfixes (14)</summary>

- [#6906](https://github.com/ROCm/aiter/pull/6906) attention with sink no longer dispatched to the asm flash_attn_varlen_func
- [#6760](https://github.com/ROCm/aiter/pull/6760) preserve virtual sinks in single-query batch prefill
- [#6703](https://github.com/ROCm/aiter/pull/6703) MLA metadata v1.0 tail fix
- [#6879](https://github.com/ROCm/aiter/pull/6879) clamp pos in the fused_qk_rope_concat_and_cache_mla_seg kernel
- [#7042](https://github.com/ROCm/aiter/pull/7042) sync wave groups in the gfx950 A16W16 HTI GEMM
- [#6368](https://github.com/ROCm/aiter/pull/6368) fix 8-wave a8w8 GEMM reading LDS before the last tile lands
- [#6902](https://github.com/ROCm/aiter/pull/6902) declare gemm_a16w16 non-mutating for torch.compile
- [#6665](https://github.com/ROCm/aiter/pull/6665) round CK-Tile a8w8 bf16 outputs to nearest even on gfx942
- [#6704](https://github.com/ROCm/aiter/pull/6704) FlyDSL a8w8 tuner fix on gfx942
- [#6860](https://github.com/ROCm/aiter/pull/6860) clear rocprofiler env vars before spawning mp_tuner workers
- [#6963](https://github.com/ROCm/aiter/pull/6963) corner cases in rotating-buffer pool size estimate
- [#6581](https://github.com/ROCm/aiter/pull/6581) normalize Gluon split constexpr values
- [#4779](https://github.com/ROCm/aiter/pull/4779) handle GroupNorm autocast safely
- [#5948](https://github.com/ROCm/aiter/pull/5948) 3D binary-op broadcast guard
- [#6323](https://github.com/ROCm/aiter/pull/6323) topk_gating kernels trap when vec_size does not divide num_experts

</details>

<details>
<summary>Rotating-buffer benchmarking (4)</summary>

- [#6551](https://github.com/ROCm/aiter/pull/6551) GEMM rotating buffers and do_bench_aiter_triton support
- [#6635](https://github.com/ROCm/aiter/pull/6635) fused-op rotating buffers
- [#6600](https://github.com/ROCm/aiter/pull/6600) MLA rotating buffers
- [#6636](https://github.com/ROCm/aiter/pull/6636) norm/RoPE rotating buffers

</details>

<details>
<summary>Refactors & misc (6)</summary>

- [#6718](https://github.com/ROCm/aiter/pull/6718) TDM new interface v2
- [#7077](https://github.com/ROCm/aiter/pull/7077) simplify PA decode reducer bound
- [#6940](https://github.com/ROCm/aiter/pull/6940) make FlyDSL PA decode kernels identifiable in traces
- [#6869](https://github.com/ROCm/aiter/pull/6869) bench_sage input distributions and deferred MoE import
- [#7055](https://github.com/ROCm/aiter/pull/7055) align OPUS CO tests and build metadata with local kernel IDs
- [#6666](https://github.com/ROCm/aiter/pull/6666) update ASM code objects

</details>

<details>
<summary>CI & build (14)</summary>

- [#7003](https://github.com/ROCm/aiter/pull/7003) shadow PR self-review gate
- [#7156](https://github.com/ROCm/aiter/pull/7156) route self-review writes through the aiter-bot PAT
- [#6992](https://github.com/ROCm/aiter/pull/6992) install mori for multi-GPU tests and add a smoke test
- [#7015](https://github.com/ROCm/aiter/pull/7015) vLLM DI smoke on the nightly image with WideEP EP8/EP16
- [#5784](https://github.com/ROCm/aiter/pull/5784) DeepSeek-V4-Pro 2P1D TP8 ATOM DI smoke cases
- [#6975](https://github.com/ROCm/aiter/pull/6975) bump FlyDSL pin from 0.4.0 to 0.4.1
- [#6930](https://github.com/ROCm/aiter/pull/6930) auto-update split test times
- [#7066](https://github.com/ROCm/aiter/pull/7066) run MI300X PR tests only on main
- [#6931](https://github.com/ROCm/aiter/pull/6931) run extended tests on main pushes
- [#4078](https://github.com/ROCm/aiter/pull/4078) backport: gate TDM/named-barrier on clang>=22 for ROCm 7.0/7.1
- plus [#7013](https://github.com/ROCm/aiter/pull/7013), [#7023](https://github.com/ROCm/aiter/pull/7023), [#6997](https://github.com/ROCm/aiter/pull/6997), [#6933](https://github.com/ROCm/aiter/pull/6933) and [#5605](https://github.com/ROCm/aiter/pull/5605) as minor CI/build updates

</details>

<details>
<summary>Newly opened: kernels & attention (25)</summary>

- [#6952](https://github.com/ROCm/aiter/pull/6952) MXFP4 MQA logits: one API for V4 and V4.1
- [#7017](https://github.com/ROCm/aiter/pull/7017) gfx942 FP4 paged MQA logits
- [#7124](https://github.com/ROCm/aiter/pull/7124) gfx950 MLA v4.1 a8w4 prefill for an NVFP4 prefix KV
- [#6958](https://github.com/ROCm/aiter/pull/6958) nvfp4 index key cache for the MSA indexer
- [#7008](https://github.com/ROCm/aiter/pull/7008) QSA FP8 KV and FP8/FP4 index caches
- [#7056](https://github.com/ROCm/aiter/pull/7056) MXFP4 KV-cache PA decode on gfx950
- [#7061](https://github.com/ROCm/aiter/pull/7061) MiniMax-M3 MXFP4 index-cache prefill scorers
- [#7060](https://github.com/ROCm/aiter/pull/7060) MiniMax-M3 MXFP4 index-cache decode scorer
- [#7057](https://github.com/ROCm/aiter/pull/7057) fused_qknorm_idxrqknorm writes MXFP4 index-K and main KV caches
- [#7000](https://github.com/ROCm/aiter/pull/7000) warp-specialized fp8 sparse MLA v4 prefill for H=128
- [#6927](https://github.com/ROCm/aiter/pull/6927) gfx950 bf16 sparse prefill (H > 32) with 4 waves
- [#7125](https://github.com/ROCm/aiter/pull/7125) balance the gfx950 XCD-lane decode planner on skewed KV lengths
- [#7079](https://github.com/ROCm/aiter/pull/7079) merge gfx1250 PA decode partitions in the tile kernel
- [#7081](https://github.com/ROCm/aiter/pull/7081) optimize gfx1250 PA partitions and packed attention
- [#7131](https://github.com/ROCm/aiter/pull/7131) Mega-MHC kernels for DeepSeek-V4.1
- [#7151](https://github.com/ROCm/aiter/pull/7151) gfx950 mHC row finalization and packed prefill fusion
- [#7114](https://github.com/ROCm/aiter/pull/7114) fn-resident mHC pre GEMM on gfx950 prefill
- [#7027](https://github.com/ROCm/aiter/pull/7027) head-192 unified_attention for MiMo-V2.6
- [#7088](https://github.com/ROCm/aiter/pull/7088) length-aware KV split for unified_attention on gfx950
- [#6972](https://github.com/ROCm/aiter/pull/6972) DCP mailbox query gather and LSE combine
- [#6919](https://github.com/ROCm/aiter/pull/6919) Mamba-2 SSD chunked forward for gfx11
- [#7011](https://github.com/ROCm/aiter/pull/7011) FlyDSL bf16 GEMM for gfx942
- [#7107](https://github.com/ROCm/aiter/pull/7107) fused GDN speculative-verify step (duplicate of [#7112](https://github.com/ROCm/aiter/pull/7112))
- [#7069](https://github.com/ROCm/aiter/pull/7069) GDR decode with optional deferred spec-decode state
- [#7028](https://github.com/ROCm/aiter/pull/7028) causal_conv1d_split_qkv updates

</details>

<details>
<summary>Newly opened: MoE, quantization & fused ops (24)</summary>

- [#7157](https://github.com/ROCm/aiter/pull/7157) FlyDSL all-reduce fusion (very large PR)
- [#6956](https://github.com/ROCm/aiter/pull/6956) build GEMM, conv, chunk_gdn_h and FP8 FMHA AOT caches by replay
- [#7063](https://github.com/ROCm/aiter/pull/7063) precompile MoE deployments (EP and TP) by model and knobs
- [#7001](https://github.com/ROCm/aiter/pull/7001) MegaMoE: faster compact Stage1 producer and FP8 GEMM1 tiles
- [#7127](https://github.com/ROCm/aiter/pull/7127) tune DSv4.1 EP8 A8W4 MegaMoE
- [#7129](https://github.com/ROCm/aiter/pull/7129) FP8 MoE on any multiple-of-8 intermediate size
- [#7019](https://github.com/ROCm/aiter/pull/7019) swiglu_limit for FP8 per_1x128 blockscale MoE
- [#6995](https://github.com/ROCm/aiter/pull/6995) explicit clamped SiLU in the a16w-mix GEMM1
- [#7135](https://github.com/ROCm/aiter/pull/7135) public two-stage fused_moe API
- [#6908](https://github.com/ROCm/aiter/pull/6908) gfx942 A16W4 MoE GEMM with v_perm byte-LUT dequant
- [#7153](https://github.com/ROCm/aiter/pull/7153) gfx942 a16w4 opt-in fp8 MFMA mode
- [#6987](https://github.com/ROCm/aiter/pull/6987) FlyDSL MoE RMSNorm support
- [#6967](https://github.com/ROCm/aiter/pull/6967) fused MoE routing kernel
- [#7065](https://github.com/ROCm/aiter/pull/7065) one-launch decode sort that also zeroes the split-k workspace
- [#7134](https://github.com/ROCm/aiter/pull/7134) route gfx950 E=128..255 decode at M>=17 to multi-phase sorting
- [#7152](https://github.com/ROCm/aiter/pull/7152) several rows per block in dynamic_per_token_scaled_quant
- [#7116](https://github.com/ROCm/aiter/pull/7116) act_mul_and_mxfp4_quant scaling_mode and roundup
- [#7108](https://github.com/ROCm/aiter/pull/7108) explicit Even activation-scale for MXFP4 MoE
- [#7012](https://github.com/ROCm/aiter/pull/7012) FLAT MXFP4 fmoe tiles on padded intermediate widths
- [#7137](https://github.com/ROCm/aiter/pull/7137) stable topk_select mode (tie='low') on gfx950
- [#7122](https://github.com/ROCm/aiter/pull/7122) gfx1250 Gluon GEMM + all-reduce + RMSNorm
- [#7082](https://github.com/ROCm/aiter/pull/7082) fuse gfx1250 LL all-reduce RMSNorm FP8 epilogue
- [#7080](https://github.com/ROCm/aiter/pull/7080) faster two-stage AR RMSNorm FP8 amax reduction
- [#6960](https://github.com/ROCm/aiter/pull/6960) all_gather_lastdim_add in custom all-reduce

</details>

<details>
<summary>Newly opened: tuning, tuner & model support (30)</summary>

- [#7111](https://github.com/ROCm/aiter/pull/7111) gfx1250 Qwen support
- [#6969](https://github.com/ROCm/aiter/pull/6969) proxy model gfx1250 work
- [#7118](https://github.com/ROCm/aiter/pull/7118) gfx1250 fused Q/K Gemma RMSNorm + MRoPE for Qwen3.5
- [#7120](https://github.com/ROCm/aiter/pull/7120) same fusion plus KV cache write
- [#7100](https://github.com/ROCm/aiter/pull/7100) SPEC_DECODE mode in UA with tuned Qwen35 config
- [#7031](https://github.com/ROCm/aiter/pull/7031) keep GLM-5.3 BF16 projections consistent across batch sizes
- [#7033](https://github.com/ROCm/aiter/pull/7033) GLM-5.3 FP8 GEMM batch consistency
- [#7035](https://github.com/ROCm/aiter/pull/7035) GLM-5.3 indexer prefill consistency after cache reuse
- [#7049](https://github.com/ROCm/aiter/pull/7049) GLM-5.3-Flash TP4 GEMM rows
- [#7084](https://github.com/ROCm/aiter/pull/7084) GLM-5.3-Flash baseline test (marked do not merge)
- [#6970](https://github.com/ROCm/aiter/pull/6970) rank accuracy-qualified kernels by package energy
- [#7091](https://github.com/ROCm/aiter/pull/7091) check fmoe tuning candidates against matching-quantization references
- [#7005](https://github.com/ROCm/aiter/pull/7005) MoE tuner fixes for DEP
- [#7041](https://github.com/ROCm/aiter/pull/7041) tuning_on_benchmarks
- [#7162](https://github.com/ROCm/aiter/pull/7162) gfx950 Llama blockscale GEMM
- [#7117](https://github.com/ROCm/aiter/pull/7117) a4w4 dispatch of triton_preshuffle rows and Qwen3.8-27B decode GEMMs
- [#7075](https://github.com/ROCm/aiter/pull/7075) MI350P Qwen3.8-27B a4w4
- [#6978](https://github.com/ROCm/aiter/pull/6978) MI455 Qwen3.8
- [#7094](https://github.com/ROCm/aiter/pull/7094) Muse Spark Open 816B bf16 on MI350P
- [#7109](https://github.com/ROCm/aiter/pull/7109) Muse Spark Open 816B MXFP4 MoE on MI350P
- [#6959](https://github.com/ROCm/aiter/pull/6959) Kimi-K3 MI355X
- [#7142](https://github.com/ROCm/aiter/pull/7142) Kimi-K3 DSpark gfx1250 rows
- [#7138](https://github.com/ROCm/aiter/pull/7138) Kimi-K3 gfx1250 gemm_a4w4
- [#6915](https://github.com/ROCm/aiter/pull/6915) Qwen3.5-35B-A3B TP4/EP4 grouped MoE
- [#7018](https://github.com/ROCm/aiter/pull/7018) DeepSeek-V4 FP8 GEMMs on gfx1250
- [#6932](https://github.com/ROCm/aiter/pull/6932) DSV4 EP8 MXFP4 rows
- [#6947](https://github.com/ROCm/aiter/pull/6947) beam bf16 gfx950
- [#6945](https://github.com/ROCm/aiter/pull/6945) gfx942 BF16 rows for the Muse Spark unpooler
- [#6981](https://github.com/ROCm/aiter/pull/6981) Qwen3.5-397B TP4 MXFP4 MoE
- plus [#7043](https://github.com/ROCm/aiter/pull/7043), [#7044](https://github.com/ROCm/aiter/pull/7044), [#7076](https://github.com/ROCm/aiter/pull/7076), [#7106](https://github.com/ROCm/aiter/pull/7106) and [#6909](https://github.com/ROCm/aiter/pull/6909) as minor tuning updates

</details>

<details>
<summary>Newly opened: bugfixes (31)</summary>

- [#7053](https://github.com/ROCm/aiter/pull/7053) deterministic fp32 split-K/slice-K reduction in gfx950 A16W16
- [#7136](https://github.com/ROCm/aiter/pull/7136) CK-Tile MXFP4 MoE stage1 split-k for unaligned K
- [#7083](https://github.com/ROCm/aiter/pull/7083) honor num_local_tokens on the MXFP4 inline-sort path
- [#7110](https://github.com/ROCm/aiter/pull/7110) num_local_tokens fix across 19 files
- [#7010](https://github.com/ROCm/aiter/pull/7010) full-height scale for per_1x128 1-stage kernels under num_local_tokens
- [#7062](https://github.com/ROCm/aiter/pull/7062) regression test for multi-phase sorting tail reads
- [#6926](https://github.com/ROCm/aiter/pull/6926) zero the a2 buffer before dynamic per-tensor quant
- [#6965](https://github.com/ROCm/aiter/pull/6965) fused_moe stage-2 reduce target device-memory exhaustion
- [#7104](https://github.com/ROCm/aiter/pull/7104) moe_reduce guard for the -1 topk_ids sentinel
- [#7130](https://github.com/ROCm/aiter/pull/7130) gfx1250 HERD decode routing past 512 experts
- [#7143](https://github.com/ROCm/aiter/pull/7143) strided A scales on mega_moe stage1_fused
- [#7147](https://github.com/ROCm/aiter/pull/7147) PA decode scaling and merge alignment
- [#7092](https://github.com/ROCm/aiter/pull/7092) zero V rows past the context before PV
- [#6971](https://github.com/ROCm/aiter/pull/6971) valid LSE from single-split BF16 QH64/QH128 decode
- [#6990](https://github.com/ROCm/aiter/pull/6990) align batch prefill full-attention dispatch
- [#6920](https://github.com/ROCm/aiter/pull/6920) LDS races in chunk_gated_delta_rule_fwd_h
- [#6911](https://github.com/ROCm/aiter/pull/6911) preserve FP32 precision in GDN prepare inverse block merges
- [#6957](https://github.com/ROCm/aiter/pull/6957) mHC pre cross-batch numerical consistency on gfx950
- [#7119](https://github.com/ROCm/aiter/pull/7119) gfx1250 GEMM output offset overflow
- [#7089](https://github.com/ROCm/aiter/pull/7089) skip empty-work gathers in gfx1250 MLA PS1
- [#7126](https://github.com/ROCm/aiter/pull/7126) never share scratch buffers whose zero fill was recorded into a graph
- [#7047](https://github.com/ROCm/aiter/pull/7047) mask OOB e8m0 scales on the ragged-K path of batched_gemm_afp4wfp4
- [#6951](https://github.com/ROCm/aiter/pull/6951) fix Triton A8W8 per-token preshuffled GEMM
- [#6944](https://github.com/ROCm/aiter/pull/6944) detect XGMI topology for custom all-reduce
- [#7149](https://github.com/ROCm/aiter/pull/7149) decline gather/scatter at group sizes with no kernel
- [#7155](https://github.com/ROCm/aiter/pull/7155) read captured gfx1250 inputs in place on IPC transport
- [#7148](https://github.com/ROCm/aiter/pull/7148) treat a zombie lock holder as dead in FileBaton
- [#7159](https://github.com/ROCm/aiter/pull/7159) CU lookup compatibility and gfx1250 kernel queries
- [#7164](https://github.com/ROCm/aiter/pull/7164) ambiguous HIP error helper lookup in the CK-free shim
- [#7074](https://github.com/ROCm/aiter/pull/7074) bench_mega_moe kernel table fix on multi-stream graphs
- [#7161](https://github.com/ROCm/aiter/pull/7161) include HIP bfloat16 header in MoE sorting

</details>

<details>
<summary>Newly opened: gfx1250/gfx11 attention, config and other (22)</summary>

- [#7160](https://github.com/ROCm/aiter/pull/7160) gfx1250 mha bwd hd64 kernels and hd128 border mask
- [#6996](https://github.com/ROCm/aiter/pull/6996) gfx1250 mha bwd d192/d128 integration
- [#7098](https://github.com/ROCm/aiter/pull/7098) FMHA prefill m32x8 skips query tiles past varlen end
- [#6998](https://github.com/ROCm/aiter/pull/6998) wave32 in the DCP decode top-k merge
- [#6976](https://github.com/ROCm/aiter/pull/6976) align gfx1250 PA decode layering with gfx942/gfx950
- [#6999](https://github.com/ROCm/aiter/pull/6999) gfx1250 unified attention 2D passes num_seqs at runtime
- [#6983](https://github.com/ROCm/aiter/pull/6983) gfx950 split-KV 3D configs for head_size <= 128
- [#7022](https://github.com/ROCm/aiter/pull/7022) fp8_mqa_logits avoids per-batch-size recompiles on gfx950
- [#7133](https://github.com/ROCm/aiter/pull/7133) gfx1250 asm MLA decode KV layout from fused_qk_rope_cat_and_cache_mla
- [#6955](https://github.com/ROCm/aiter/pull/6955) sparse MLA native fp8 dtype from get_fp8_e4m3_dtype()
- [#6961](https://github.com/ROCm/aiter/pull/6961) on-device kernel selection in mla_gluon
- [#7034](https://github.com/ROCm/aiter/pull/7034) KDA cleanup
- [#6912](https://github.com/ROCm/aiter/pull/6912) KDA accepts cu_seqlens_cpu
- [#7064](https://github.com/ROCm/aiter/pull/7064) gfx1250 no-quant RMSNorm dispatch for wave32
- [#7090](https://github.com/ROCm/aiter/pull/7090) cache gfx1250 GEMM layout metadata on the host
- [#7093](https://github.com/ROCm/aiter/pull/7093) QuickAllReduce INT4: faster poll and codec
- [#7050](https://github.com/ROCm/aiter/pull/7050) QuickReduce INT4 default super_tile 1
- [#7032](https://github.com/ROCm/aiter/pull/7032) Triton Conv padding mode
- [#7040](https://github.com/ROCm/aiter/pull/7040) padding mode in specialized Conv2D
- [#6973](https://github.com/ROCm/aiter/pull/6973) gfx1151 Conv3D configs
- [#7154](https://github.com/ROCm/aiter/pull/7154) gfx1150 Conv3D configs
- plus [#7123](https://github.com/ROCm/aiter/pull/7123), [#7086](https://github.com/ROCm/aiter/pull/7086), [#7165](https://github.com/ROCm/aiter/pull/7165), [#7163](https://github.com/ROCm/aiter/pull/7163), [#7166](https://github.com/ROCm/aiter/pull/7166), [#7029](https://github.com/ROCm/aiter/pull/7029), [#6968](https://github.com/ROCm/aiter/pull/6968), [#7097](https://github.com/ROCm/aiter/pull/7097), [#7039](https://github.com/ROCm/aiter/pull/7039), [#7103](https://github.com/ROCm/aiter/pull/7103), [#7101](https://github.com/ROCm/aiter/pull/7101), [#7139](https://github.com/ROCm/aiter/pull/7139), [#7024](https://github.com/ROCm/aiter/pull/7024), [#6917](https://github.com/ROCm/aiter/pull/6917), [#6914](https://github.com/ROCm/aiter/pull/6914), [#6941](https://github.com/ROCm/aiter/pull/6941), [#6922](https://github.com/ROCm/aiter/pull/6922), [#7121](https://github.com/ROCm/aiter/pull/7121), [#6986](https://github.com/ROCm/aiter/pull/6986), [#6985](https://github.com/ROCm/aiter/pull/6985), [#7078](https://github.com/ROCm/aiter/pull/7078), [#7030](https://github.com/ROCm/aiter/pull/7030), [#6982](https://github.com/ROCm/aiter/pull/6982), [#7071](https://github.com/ROCm/aiter/pull/7071), [#7072](https://github.com/ROCm/aiter/pull/7072), [#6979](https://github.com/ROCm/aiter/pull/6979), [#7059](https://github.com/ROCm/aiter/pull/7059), [#7048](https://github.com/ROCm/aiter/pull/7048), [#7146](https://github.com/ROCm/aiter/pull/7146), [#7128](https://github.com/ROCm/aiter/pull/7128), [#7122](https://github.com/ROCm/aiter/pull/7122) and [#7143](https://github.com/ROCm/aiter/pull/7143) as minor test, CI, config and misc updates

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (AITER.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: d6151331a810fed14b5296238925ce93dcf7a4eabdc9361b034dd218b3a64613 -->
