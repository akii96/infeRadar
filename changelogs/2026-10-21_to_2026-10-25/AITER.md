# AITER: PR digest (2026-10-21 to 2026-10-25)

_102 merged, 110 newly opened - source ROCm/AITER, generated 2026-10-25T23:07:03Z_

## TL;DR
- **DeepSeek (V4 / V4.1 / R1) got the most attention**, followed by Kimi (K2 / K3) and Qwen3.5 / 3.8. Merged work includes a fused Mega-MHC kernel, a gfx1250 Gluon a8w8 sparse MLA kernel, MXFP4 a4w4 GEMM, and R1 GEMM tunings.
- **gfx1250 is the main bring-up target.** It gets sparse MLA, FP8/BF16 paged-attention decode, QuickReduce for TP2/TP4, MXFP4 and mxfp8 GEMMs, and many Gluon GEMM tuning sets for Llama3, DSR1, Kimi and Qwen. Newly opened work adds a "gfx1250-strict" arch plumbing change.
- **Quantization and GEMM dominate the churn.** A W4A16 GPTQ/AWQ GEMM landed, along with an A8W8 per-token preshuffled GEMM and a fused gated RMSNorm + MXFP4 quant. Tuning configs account for 75 labelled PRs.
- **In-progress work is aimed at fused megakernels and attention variants.** Examples are a MegaMoEV2 that fuses dispatch, GEMM1, GEMM2 and combine, a gfx950 sparse online MHA v4, and a fused norm/rope/cast kernel. Many correctness fixes are merging alongside (int32 overflow, FP8 probability scaling, MoE dispatch).

## Most important PRs
**[#6116](https://github.com/ROCm/aiter/pull/6116): Gluon a8w8 Sparse MLA for gfx1250.**
Adds an FP8-activation, FP8-weight sparse MLA decode kernel in Gluon for DeepSeek-style sparse attention on gfx1250. It is the largest merged change of the window, with 37 commits.

**[#6520](https://github.com/ROCm/aiter/pull/6520): Fused Mega-MHC for DeepSeek V4.1.**
A new HIP JIT kernel that fuses the multi-head hyper-connection path for V4.1, cutting launch count and memory traffic around the mixing step.

**[#6778](https://github.com/ROCm/aiter/pull/6778): gemm_a16w4 int4 weight-only GEMM.**
Adds a Triton W4A16 GEMM for GPTQ/AWQ checkpoints on gfx942, with tuned configs. This opens int4 weight-only models to the Triton path.

**[#6621](https://github.com/ROCm/aiter/pull/6621): gfx1250 MXFP4 a4w4 GEMM with tuned DSR1 configs.**
A FlyDSL/HIP MXFP4 GEMM for the new arch, with DeepSeek-R1 shape tuning.

**[#6107](https://github.com/ROCm/aiter/pull/6107): `get_mla_decode_shape_support` backed by shared C++ head-fold rules.**
Centralizes which MLA decode shapes and backends are supported, so Python and C++ dispatch no longer drift apart.

## More changes by area

<details>
<summary>Performance (9)</summary>

- [#6656](https://github.com/ROCm/aiter/pull/6656) split short batches across workgroups in scaled_silu_and_mul
- [#5921](https://github.com/ROCm/aiter/pull/5921) fp8_mqa_logits derives its split target from kernel occupancy
- [#6888](https://github.com/ROCm/aiter/pull/6888) gfx1250 unified_attention: fast split-KV reduce at small batch
- [#6749](https://github.com/ROCm/aiter/pull/6749) tune A4W4 prefill MMA groups and B TDM TH
- [#6061](https://github.com/ROCm/aiter/pull/6061) tune gfx950 GEMM configs for N=K=2048
- [#6726](https://github.com/ROCm/aiter/pull/6726) tune DSR1 input projection
- [#6744](https://github.com/ROCm/aiter/pull/6744) sweep NUM_BUFFERS and kernel_type for gfx1250 persistent GEMMs
- [#6694](https://github.com/ROCm/aiter/pull/6694) align persistent workgroup count for fmoe kernels that remap across XCDs
- [#6741](https://github.com/ROCm/aiter/pull/6741) retune gfx950 AFP4WFP4 decode buckets for Llama-3.3-70B

</details>

<details>
<summary>Kernels & attention (22)</summary>

- [#6670](https://github.com/ROCm/aiter/pull/6670) fused QSA sparse decode (FlyDSL, gfx950)
- [#5992](https://github.com/ROCm/aiter/pull/5992) causal conv1d prefill and GDN decode/verify for Qwen3.5/3.8
- [#6488](https://github.com/ROCm/aiter/pull/6488) fused GDN decode for any value/key head ratio
- [#6672](https://github.com/ROCm/aiter/pull/6672) BF16 state storage in gfx950 KDA
- [#5993](https://github.com/ROCm/aiter/pull/5993) hc_mix kernel for Qwen3.8 hyper-connections
- [#6863](https://github.com/ROCm/aiter/pull/6863) paged FP8 MQA logits with 8-token KV pages
- [#6462](https://github.com/ROCm/aiter/pull/6462) gfx1250 paged attention decode with FP8 and BF16
- [#5965](https://github.com/ROCm/aiter/pull/5965) gfx1250 QuickReduce for TP2/TP4
- [#6570](https://github.com/ROCm/aiter/pull/6570) support up to TP64 on all-gather
- [#6038](https://github.com/ROCm/aiter/pull/6038) fused gated RMSNorm + MXFP4 quant
- [#6674](https://github.com/ROCm/aiter/pull/6674) fused_gemm_a16w16_mul_add for the DiT gated residual
- [#6850](https://github.com/ROCm/aiter/pull/6850) A8W8 per-token preshuffled Triton GEMM
- [#6864](https://github.com/ROCm/aiter/pull/6864) batched mxfp8_32 GEMM with 32x32 weight scales
- [#6582](https://github.com/ROCm/aiter/pull/6582) scale-mode arguments in hipb_mm
- [#6504](https://github.com/ROCm/aiter/pull/6504) Triton Conv2D padding primitives
- [#6813](https://github.com/ROCm/aiter/pull/6813) rotating-buffer helpers and do_bench_aiter_triton
- [#6737](https://github.com/ROCm/aiter/pull/6737) Flash Attention follow-up
- [#6748](https://github.com/ROCm/aiter/pull/6748) round CK FMHA bf16 conversions to nearest
- [#6257](https://github.com/ROCm/aiter/pull/6257) optimized biased grouped topk on gfx1250
- [#3993](https://github.com/ROCm/aiter/pull/3993) wire is_causal through mla_decode_fwd
- [#6380](https://github.com/ROCm/aiter/pull/6380) simplify FlyDSL kernel APIs and remove redundant wrappers
- [#6809](https://github.com/ROCm/aiter/pull/6809) clean up test_pa_decode_gluon

</details>

<details>
<summary>MoE & quantization (14)</summary>

- [#6890](https://github.com/ROCm/aiter/pull/6890) DSV4 Flash MoE tuned config
- [#6693](https://github.com/ROCm/aiter/pull/6693) Qwen3.8-Flash-Next FP8 fused-MoE configs for gfx942
- [#6593](https://github.com/ROCm/aiter/pull/6593) Muse Spark Open MXFP4 FMoE tuning
- [#6622](https://github.com/ROCm/aiter/pull/6622) v41 tp2 MoE config for shared-expert fusion
- [#6681](https://github.com/ROCm/aiter/pull/6681) drop token=1,2 tuned fmoe rows for Qwen3-235B FP8 EP
- [#6688](https://github.com/ROCm/aiter/pull/6688) gpt-oss a16w4 MoE decode tiles for Triton 3.8
- [#6468](https://github.com/ROCm/aiter/pull/6468) Qwen3.8 TP=8 MXFP4 MoE aux kernel codegen
- [#6395](https://github.com/ROCm/aiter/pull/6395) write grouped MoE tuning results back in place
- [#6695](https://github.com/ROCm/aiter/pull/6695) dsv4.1 MoE router and KV compressor a16w16 configs
- [#6862](https://github.com/ROCm/aiter/pull/6862) Qwen3-14B-FP8 a8w8 blockscale bpreshuffle tunings
- [#6769](https://github.com/ROCm/aiter/pull/6769) Qwen3.8 Flash Next a8w8 and BF16 tunings
- [#6757](https://github.com/ROCm/aiter/pull/6757) gfx942 a8w8 blockscale Triton configs for Qwen3 shapes
- [#6606](https://github.com/ROCm/aiter/pull/6606) fix gfx950 GQA16 MTP softmax initialization
- [#6826](https://github.com/ROCm/aiter/pull/6826) restore gfx950 PA 2TG vector loads

</details>

<details>
<summary>Hardware & arch (20)</summary>

- [#6687](https://github.com/ROCm/aiter/pull/6687) gfx1250 Gluon GEMMs for DeepSeek-R1
- [#6725](https://github.com/ROCm/aiter/pull/6725) gfx1250 Gluon GEMMs for Kimi-K2 Thinking
- [#6763](https://github.com/ROCm/aiter/pull/6763) Kimi-K3 TP8 GEMM tune
- [#6717](https://github.com/ROCm/aiter/pull/6717) MiniMax-M3 PTPC GEMMs
- [#6652](https://github.com/ROCm/aiter/pull/6652) gfx1250 MXFP4 GEMMs for Llama3 8B
- [#6653](https://github.com/ROCm/aiter/pull/6653) gfx1250 MXFP4 GEMMs for Llama3 70B
- [#6654](https://github.com/ROCm/aiter/pull/6654) gfx1250 MXFP4 GEMMs for Llama3 405B
- [#6649](https://github.com/ROCm/aiter/pull/6649) gfx1250 a16w16 GEMMs for Qwen3-235B-A22B
- [#6650](https://github.com/ROCm/aiter/pull/6650) gfx1250 a16w16 GEMMs for Llama4 Maverick
- [#6601](https://github.com/ROCm/aiter/pull/6601) gfx950 gemm_a16w16 configs for DeepSeek-V4 (K=7168)
- [#6780](https://github.com/ROCm/aiter/pull/6780) gfx950 BF16 batched GEMM for Kimi-K2.6
- [#5961](https://github.com/ROCm/aiter/pull/5961) gemm_a16w16 gfx1101 (RDNA3) configs
- [#6671](https://github.com/ROCm/aiter/pull/6671) gfx1151 gemm_a16w16 DEFAULT.json
- [#6772](https://github.com/ROCm/aiter/pull/6772) gfx1100 RMSNorm large-M/small-N config
- [#6773](https://github.com/ROCm/aiter/pull/6773) gfx950 compat shim for get_scaled_upcast_fp4_scale_layout
- [#6607](https://github.com/ROCm/aiter/pull/6607) gfx1250 A4W4 192x256 no-ps and dispatch fix
- [#6756](https://github.com/ROCm/aiter/pull/6756) gfx1250 low-latency all-reduce fix
- [#6348](https://github.com/ROCm/aiter/pull/6348) gfx1250 RMSNorm row tails and block-reduction fence
- [#6679](https://github.com/ROCm/aiter/pull/6679) gfx1250 a8w8 blockscale NUM_BUFFERS config key
- [#6874](https://github.com/ROCm/aiter/pull/6874) gfx950 AFP4WFP4 tiles for Qwen3.8-27B-MXFP4 TP1

</details>

<details>
<summary>Bugfixes (20)</summary>

- [#5320](https://github.com/ROCm/aiter/pull/5320) int32 overflow in deepgemm FP8 paged MQA logits offsets
- [#5642](https://github.com/ROCm/aiter/pull/5642) scale FP8 softmax probabilities into the e4m3 normal range in paged_attention_ragged
- [#6138](https://github.com/ROCm/aiter/pull/6138) scale gfx942 Sage probabilities before FP8 conversion
- [#6639](https://github.com/ROCm/aiter/pull/6639) wrong results in gfx942 fp8 persistent/blockscale fused-MoE dispatch
- [#6691](https://github.com/ROCm/aiter/pull/6691) check model_dim for gfx950 fp8 blockscale fused-MoE 1-stage kernels
- [#6663](https://github.com/ROCm/aiter/pull/6663) dropped K tail and bias offset in the grouped MoE TDM GEMM
- [#6758](https://github.com/ROCm/aiter/pull/6758) split-K partial offsets in int64
- [#6661](https://github.com/ROCm/aiter/pull/6661) unified_attention wrong output with 2-4 GiB packed KV cache
- [#6428](https://github.com/ROCm/aiter/pull/6428) NaN dq in Triton MHA backward
- [#6325](https://github.com/ROCm/aiter/pull/6325) mask KV padding lanes in paged_attention_decode
- [#6198](https://github.com/ROCm/aiter/pull/6198) reject non-576-wide rows in mla_decode_stage1_asm_fwd
- [#6750](https://github.com/ROCm/aiter/pull/6750) disable spurious output clamp in the MLA ASM kernel
- [#6833](https://github.com/ROCm/aiter/pull/6833) graph-safe topk end=None and related fixes
- [#6700](https://github.com/ROCm/aiter/pull/6700) replay biased interleaved MoE callers and fix CI
- [#6834](https://github.com/ROCm/aiter/pull/6834) fix topk_sigmoid pybind conversion
- [#6592](https://github.com/ROCm/aiter/pull/6592) earlier topk_sigmoid pybind fix
- [#6811](https://github.com/ROCm/aiter/pull/6811) revert of the topk_sigmoid fix
- [#6398](https://github.com/ROCm/aiter/pull/6398) bind load_hip_runtime to the already-loaded HIP runtime
- [#6738](https://github.com/ROCm/aiter/pull/6738) import aiter with no visible GPU
- [#5991](https://github.com/ROCm/aiter/pull/5991) missing extension module names in pretune builds

</details>

<details>
<summary>Tests (8)</summary>

- [#6783](https://github.com/ROCm/aiter/pull/6783) fix cuda and dtype assignments in triton UTs
- [#6846](https://github.com/ROCm/aiter/pull/6846) review follow-up to the cuda assignment fix
- [#6797](https://github.com/ROCm/aiter/pull/6797) fix UT leaks
- [#6795](https://github.com/ROCm/aiter/pull/6795) fix UT leaks
- [#6796](https://github.com/ROCm/aiter/pull/6796) fix mha UT
- [#6747](https://github.com/ROCm/aiter/pull/6747) stop test_extend_attention changing the default dtype
- [#6690](https://github.com/ROCm/aiter/pull/6690) bench_pa_decode reports real KV bandwidth with CUDA graphs
- [#6479](https://github.com/ROCm/aiter/pull/6479) stop reporting a fast-kernel failure that never ran in test_topk_row_prefill

</details>

<details>
<summary>CI & build (4)</summary>

- [#5634](https://github.com/ROCm/aiter/pull/5634) enable MiniMax-M3 MXFP8 2P1D TP8 ATOM DI CI
- [#6364](https://github.com/ROCm/aiter/pull/6364) relax Standard Test Results reporting
- [#6878](https://github.com/ROCm/aiter/pull/6878) increase MI35X Triton test timeout
- [#4486](https://github.com/ROCm/aiter/pull/4486) make the C++ paged_attention_ragged entry point usable and tested

</details>

<details>
<summary>Newly opened: kernels & attention (32)</summary>

- [#6821](https://github.com/ROCm/aiter/pull/6821) fused_norm_rope_att_rope_cast kernel
- [#6822](https://github.com/ROCm/aiter/pull/6822) MHA v4 sparsified online attention for gfx950
- [#6841](https://github.com/ROCm/aiter/pull/6841) MHA v4 LSE on sorted-sparse and race fixes
- [#6835](https://github.com/ROCm/aiter/pull/6835) fused Qwen3-Next attention prologue
- [#6849](https://github.com/ROCm/aiter/pull/6849) broadcast-Q causal jagged attention
- [#6848](https://github.com/ROCm/aiter/pull/6848) M-FALCON candidate attention
- [#6764](https://github.com/ROCm/aiter/pull/6764) non-causal mode for multi-token PA decode
- [#6830](https://github.com/ROCm/aiter/pull/6830) eight-row FP8 MQA logits path for gfx950
- [#6899](https://github.com/ROCm/aiter/pull/6899) window-aware split-KV for sliding-window attention
- [#6889](https://github.com/ROCm/aiter/pull/6889) split window-trimmed sliding-window verify on gfx950
- [#6896](https://github.com/ROCm/aiter/pull/6896) gfx1250 unified_attention spec-decode verify
- [#6876](https://github.com/ROCm/aiter/pull/6876) deterministic batch-invariant decode option for unified_attention
- [#6842](https://github.com/ROCm/aiter/pull/6842) sigmoid output gate for pa_decode_gluon
- [#6868](https://github.com/ROCm/aiter/pull/6868) non-causal right sliding window in Triton MHA
- [#6867](https://github.com/ROCm/aiter/pull/6867) right window with causal sliding-window MHA
- [#6905](https://github.com/ROCm/aiter/pull/6905) fused GDN decode on gfx1250
- [#6884](https://github.com/ROCm/aiter/pull/6884) bf16 recurrent state in the fused GDN decode kernel
- [#6919](https://github.com/ROCm/aiter/pull/6919) Mamba-2 SSD chunked forward for gfx11
- [#6897](https://github.com/ROCm/aiter/pull/6897) gfx1250 FMHA prefill with v_hdim 256
- [#6770](https://github.com/ROCm/aiter/pull/6770) fav3_sage RDNA3 support
- [#6782](https://github.com/ROCm/aiter/pull/6782) is_sw_emulated_fp8_avail for gfx11
- [#6785](https://github.com/ROCm/aiter/pull/6785) read V transposed with ds_read_b64_tr_b16 in paged_attention_ll4mi
- [#6815](https://github.com/ROCm/aiter/pull/6815) opt-in prefix-budget metadata planner for PA
- [#6831](https://github.com/ROCm/aiter/pull/6831) pipeline CSR segments in OPUS sparse prefill
- [#6893](https://github.com/ROCm/aiter/pull/6893) route varlen FMHA v3 to CK when an attention sink is set
- [#6855](https://github.com/ROCm/aiter/pull/6855) multi-row TDM fused_qk_norm_rope_group_quant for gfx1250
- [#6808](https://github.com/ROCm/aiter/pull/6808) optional pre-quant k_out_unquantized for fused_qk_norm_rope_cache
- [#6779](https://github.com/ROCm/aiter/pull/6779) MRoPE, shuffle KV layout and optional outputs for fused_qkv_split_qk_norm_rope_cache
- [#6832](https://github.com/ROCm/aiter/pull/6832) reuse query quantization in fused FP8 BMM
- [#6912](https://github.com/ROCm/aiter/pull/6912) KDA accepts cu_seqlens_cpu
- [#6851](https://github.com/ROCm/aiter/pull/6851) tune gfx950 one-kernel MHA backward num_stages
- [#6753](https://github.com/ROCm/aiter/pull/6753) unified_attention num_stages 2 for large prefill tiles

</details>

<details>
<summary>Newly opened: MoE & quantization (22)</summary>

- [#6881](https://github.com/ROCm/aiter/pull/6881) MegaMoEV2 fusing dispatch, GEMM1, GEMM2 and combine
- [#6900](https://github.com/ROCm/aiter/pull/6900) MegaMoE EP8 prepare chain and MXFP8 quant coalescing
- [#6754](https://github.com/ROCm/aiter/pull/6754) Muse MoE GEMM and finalize on MXFP4 weights
- [#6861](https://github.com/ROCm/aiter/pull/6861) optional per_slot_output for fused_moe
- [#6916](https://github.com/ROCm/aiter/pull/6916) pad-row routing count, custom all_gatherv, quant-sort race fix
- [#6908](https://github.com/ROCm/aiter/pull/6908) gfx942 A16W4 MoE GEMM with byte-LUT dequant
- [#6837](https://github.com/ROCm/aiter/pull/6837) a16w4 stage2 reduce for fp4
- [#6828](https://github.com/ROCm/aiter/pull/6828) gfx950 4-wave INT8 bpreshuffle GEMM
- [#6824](https://github.com/ROCm/aiter/pull/6824) OPUS 1x32 bmm bpreshuffle
- [#6856](https://github.com/ROCm/aiter/pull/6856) 32x32 w_scale mxfp8 bpreshuffle GEMM with DSv4.1 Flash configs
- [#6825](https://github.com/ROCm/aiter/pull/6825) gfx950 MXFP6 GEMM tuning candidates
- [#6907](https://github.com/ROCm/aiter/pull/6907) CK per-tensor KPerBlock=256 a8w8 gemm2 instances
- [#6866](https://github.com/ROCm/aiter/pull/6866) hadamard_rotate in fused_rms_gated_mxfp4_quant
- [#6786](https://github.com/ROCm/aiter/pull/6786) out_zeroed skips split-K output memset
- [#6817](https://github.com/ROCm/aiter/pull/6817) Muse Spark Open FMoE rows
- [#6820](https://github.com/ROCm/aiter/pull/6820) Kimi-K3 gfx950 BF16 tuned rows
- [#6768](https://github.com/ROCm/aiter/pull/6768) Kimi-K3 TP8 gfx1250 grouped-MoE tuning
- [#6915](https://github.com/ROCm/aiter/pull/6915) Qwen3.5-35B-A3B grouped MoE tuning
- [#6894](https://github.com/ROCm/aiter/pull/6894) route small TP batches in one launch on gfx1250 grouped MoE
- [#6917](https://github.com/ROCm/aiter/pull/6917) 256-thread MX combine tile
- [#6914](https://github.com/ROCm/aiter/pull/6914) match ep_fused=1 grouped MoE config rows
- [#6898](https://github.com/ROCm/aiter/pull/6898) ASM split-K rows for Qwen3-14B-FP8

</details>

<details>
<summary>Newly opened: tuning configs (14)</summary>

- [#6913](https://github.com/ROCm/aiter/pull/6913) gfx1250 DeepSeek-R1 TP4
- [#6901](https://github.com/ROCm/aiter/pull/6901) Qwen3.5-35B-A3B TP4
- [#6910](https://github.com/ROCm/aiter/pull/6910) Qwen3.5-35B-A3B TP1
- [#6903](https://github.com/ROCm/aiter/pull/6903) Kimi-K2 Thinking TP4
- [#6870](https://github.com/ROCm/aiter/pull/6870) GPT-OSS 120B TP4
- [#6871](https://github.com/ROCm/aiter/pull/6871) Llama3 8B TP4 MXFP4
- [#6872](https://github.com/ROCm/aiter/pull/6872) Llama3 70B TP4 MXFP4
- [#6873](https://github.com/ROCm/aiter/pull/6873) Llama3 405B TP4 MXFP4
- [#6771](https://github.com/ROCm/aiter/pull/6771) gfx1100 Llama-3-8B and Qwen3 A16W16
- [#6759](https://github.com/ROCm/aiter/pull/6759) retune gfx950 Triton ops that regressed with Triton 3.8
- [#6784](https://github.com/ROCm/aiter/pull/6784) gfx1250 PA decode tuning
- [#6765](https://github.com/ROCm/aiter/pull/6765) floor gfx942 bf16 unified-attention decode tile at 32
- [#6909](https://github.com/ROCm/aiter/pull/6909) AI-tuned FP8 blockscale GEMM code objects for gfx942
- [#6762](https://github.com/ROCm/aiter/pull/6762) cache per-config host work on the FlyDSL GEMM launch path

</details>

<details>
<summary>Newly opened: bugfixes (17)</summary>

- [#6853](https://github.com/ROCm/aiter/pull/6853) gfx950 A16W16 int32 C-offset overflow
- [#6854](https://github.com/ROCm/aiter/pull/6854) uneven split-K in fused a8w8 blockscale GEMMs
- [#6880](https://github.com/ROCm/aiter/pull/6880) in-kernel gather for MXFP4 MoE GEMM on gfx1250
- [#6891](https://github.com/ROCm/aiter/pull/6891) dropped and misplaced KV ranges in MLA v1_0/v1_2 metadata
- [#6906](https://github.com/ROCm/aiter/pull/6906) sink attention must not dispatch to the ASM flash_attn_varlen_func
- [#6760](https://github.com/ROCm/aiter/pull/6760) preserve virtual sinks in single-query batch prefill
- [#6798](https://github.com/ROCm/aiter/pull/6798) query-head offset for GQA ratios above 16
- [#6766](https://github.com/ROCm/aiter/pull/6766) persistent asm fused_moe launches with total_tgs workgroups
- [#6836](https://github.com/ROCm/aiter/pull/6836) clamp NaN/Inf in grouped_topk biased sigmoid path
- [#6761](https://github.com/ROCm/aiter/pull/6761) topk_select must not evict default end-index rows captured by graphs
- [#6920](https://github.com/ROCm/aiter/pull/6920) LDS races in HIP chunk_gated_delta_rule_fwd_h
- [#6911](https://github.com/ROCm/aiter/pull/6911) preserve FP32 precision in GDN prepare inverse block merges
- [#6879](https://github.com/ROCm/aiter/pull/6879) clamp pos in the fused rope MLA cache kernel
- [#6877](https://github.com/ROCm/aiter/pull/6877) hardcoded die count in HIP kernels
- [#6755](https://github.com/ROCm/aiter/pull/6755) mask stale V rows past sequence end in gfx950 Gluon unified attention
- [#6751](https://github.com/ROCm/aiter/pull/6751) fix fused_qk_norm_rope_group_quant
- [#6902](https://github.com/ROCm/aiter/pull/6902) declare gemm_a16w16 non-mutating for torch.compile

</details>

<details>
<summary>Newly opened: platform, CI & tooling (23)</summary>

- [#6767](https://github.com/ROCm/aiter/pull/6767) gfx1250-strict architecture plumbing
- [#6819](https://github.com/ROCm/aiter/pull/6819) keep CUDA-graph buffer registration in step across ranks for custom AR
- [#6810](https://github.com/ROCm/aiter/pull/6810) FlyDSL FCA
- [#6847](https://github.com/ROCm/aiter/pull/6847) precompile only FlyDSL GEMM and conv jobs for GPU_ARCHS
- [#6844](https://github.com/ROCm/aiter/pull/6844) build every listed CU count per GPU_ARCHS arch
- [#6904](https://github.com/ROCm/aiter/pull/6904) add gfx1101 to allowed_archs
- [#6895](https://github.com/ROCm/aiter/pull/6895) tuner event pid recovery and deadlock fix
- [#6860](https://github.com/ROCm/aiter/pull/6860) clear rocprofiler env vars before spawning mp_tuner workers
- [#6882](https://github.com/ROCm/aiter/pull/6882) upgrade shared PyTorch images to ROCm 10.1 and PyTorch 2.14
- [#6812](https://github.com/ROCm/aiter/pull/6812) include tests/ in test sharding
- [#6859](https://github.com/ROCm/aiter/pull/6859) fix Flash Attention main CI
- [#6845](https://github.com/ROCm/aiter/pull/6845) padding-mode support in routed Triton Conv2D
- [#6838](https://github.com/ROCm/aiter/pull/6838) rotating buffers for ATTN DELTA benchmark
- [#6840](https://github.com/ROCm/aiter/pull/6840) rotating buffers for SPARSE ATTN benchmark
- [#6839](https://github.com/ROCm/aiter/pull/6839) rotating buffers for UNIFIED ATTENTION benchmark
- [#6843](https://github.com/ROCm/aiter/pull/6843) rotating buffers for GATED DELTA benchmark
- [#6814](https://github.com/ROCm/aiter/pull/6814) benchmark model config changes
- [#6816](https://github.com/ROCm/aiter/pull/6816) bench MOE EP with no-mega support
- [#6869](https://github.com/ROCm/aiter/pull/6869) bench_sage diffusion-calibrated inputs
- [#6875](https://github.com/ROCm/aiter/pull/6875) fix model benchmark scripts
- [#6885](https://github.com/ROCm/aiter/pull/6885) accept equal-score ties in test_topk_softmax_shared_gate
- [#6883](https://github.com/ROCm/aiter/pull/6883) stop test_kvcache counting uninitialized bytes
- [#6886](https://github.com/ROCm/aiter/pull/6886) use device fp8 range in test_fused_kv_norm_rope_group_quant
- [#6887](https://github.com/ROCm/aiter/pull/6887) MLA round-robin golden returns zero for fully masked rows
- [#6865](https://github.com/ROCm/aiter/pull/6865) review-pr: add HK20 and A4 checks

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (AITER.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 382502e56fefa2866e2ea0fdd1129db540b5a906ca09664c1e56a1fcaed32170 -->
