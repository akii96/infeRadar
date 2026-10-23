# AITER: PR digest (2026-10-18 to 2026-10-22)

_91 merged, 111 newly opened - source ROCm/AITER, generated 2026-10-22T14:26:29Z_

## TL;DR
- **DeepSeek, Qwen, Kimi and MiniMax got the most attention.** DeepSeek work was MLA decode and V4.1 MoE configs. Qwen3.8-Flash-Next got GEMM and fused-MoE tunings, and Kimi-K2/K3 got gfx1250 GEMM and MoE tunings. MiniMax-M3 got gfx1250 PTPC GEMM tuning and MoE work.
- **gfx1250 (new silicon) is the dominant theme.** Merged work includes persistent MLA decode with BF16 and TP4/TP2 MTP, FlyDSL FMHA prefill, FP8/BF16 paged-attention decode, QuickReduce for TP2/TP4, and many Gluon GEMM tunings.
- **MoE and quantization:** merged work covers the MI308 MoE-down kernels with BF16, `mega_moe_tp` big-M optimizations, and fused add-RMSNorm plus MXFP4 quant inside INT4 QuickReduce. New in-flight work includes HipKittens block-FP8 MoE, a Blockscale MXFP8 OPUS GEMM, and a W4A16 Triton GEMM.
- **Direction:** FlyDSL and Gluon are replacing hand-written HIP/ASM for new kernels, and Triton 3.8 retunes are landing to fix VGPR-spill regressions. Many correctness fixes landed for FP8 saturation, int32/int64 offsets and bf16 rounding.

## Most important PRs
**[#6563](https://github.com/ROCm/aiter/pull/6563): gfx1250 persistent MLA decode, with BF16 and TP4/TP2 MTP.**
Optimizes the persistent MLA decode path across ASM, HIP and FlyDSL and adds BF16 and multi-token-prediction support at TP4/TP2. This is the main DeepSeek-class decode path on the new architecture.

**[#6536](https://github.com/ROCm/aiter/pull/6536): Rebuild the gfx950 BF16 opus MLA decode kernels with named-register pins.**
Rewrites the MLA decode ASM with explicit register pinning, giving more deterministic codegen on MI355-class parts.

**[#5932](https://github.com/ROCm/aiter/pull/5932): Optimize MI308 MoE down kernels and add BF16 (2/3).**
New FlyDSL/CK MoE stage-2 kernels for gfx942, aimed at Qwen and MiniMax MoE shapes.

**[#6514](https://github.com/ROCm/aiter/pull/6514): `mega_moe_tp` unified path and big-M optimizations.**
Unifies the FlyDSL fused MoE-with-communication path and optimizes large-token batches (prefill).

**[#6355](https://github.com/ROCm/aiter/pull/6355): gfx1250 FlyDSL FMHA m32x8 prefill.**
Adds d64 support, wider shape coverage and a rewritten KV pipeline for prefill attention. Newly opened [#6702](https://github.com/ROCm/aiter/pull/6702) extends this to FP8/BF8.

**Newly opened, worth watching:** [#6689](https://github.com/ROCm/aiter/pull/6689) (a 39k-line GEMM+epilogue fusion framework with FP8 QKV GEMM and Ulysses SP exchange for gfx950), [#6822](https://github.com/ROCm/aiter/pull/6822) (MHA v4 sparsified online attention) and [#6675](https://github.com/ROCm/aiter/pull/6675) (gfx950 MLA v4.1 sparse prefill).

## More changes by area

<details>
<summary>Performance (9)</summary>

- [#6656](https://github.com/ROCm/aiter/pull/6656) split short batches across workgroups in `scaled_silu_and_mul`
- [#6697](https://github.com/ROCm/aiter/pull/6697) (open) fold the MXFP4 MoE sort into GEMM1 for GLM-5.2 TP8 small-M decode
- [#6785](https://github.com/ROCm/aiter/pull/6785) (open) read V transposed with `ds_read_b64_tr_b16` in paged_attention_ll4mi on gfx950
- [#6762](https://github.com/ROCm/aiter/pull/6762) (open) cache per-config host work on the FlyDSL GEMM launch path
- [#6831](https://github.com/ROCm/aiter/pull/6831) (open) pipeline CSR segments in unsplit OPUS sparse prefill
- [#6723](https://github.com/ROCm/aiter/pull/6723) (open) MXFP4 output epilogue for gfx1250 FP4 GEMM, feeding MegaMoE fp4 dispatch
- [#6765](https://github.com/ROCm/aiter/pull/6765) (open) floor the gfx942 bf16 unified-attention decode tile at 32
- [#6668](https://github.com/ROCm/aiter/pull/6668) (open) MiniMax-M3 MoE on gfx1250: fused route psum and tuned grouped A8W4 tiles
- [#6753](https://github.com/ROCm/aiter/pull/6753) (open) Muse Spark MI355X prefill: a16w4 per-slot stage-2 epilogue

</details>

<details>
<summary>Kernels & attention (46)</summary>

- [#6488](https://github.com/ROCm/aiter/pull/6488) fused GDN decode kernel for any value/key head ratio (Qwen3.5/3.8)
- [#6655](https://github.com/ROCm/aiter/pull/6655) packed D256 PA decode pipeline for gfx950
- [#6462](https://github.com/ROCm/aiter/pull/6462) gfx1250 paged-attention decode with FP8 and BF16
- [#6369](https://github.com/ROCm/aiter/pull/6369) fuse add-RMSNorm and MXFP4 quant into INT4 QuickReduce
- [#5965](https://github.com/ROCm/aiter/pull/5965) gfx1250 QuickReduce for TP2/TP4
- [#6421](https://github.com/ROCm/aiter/pull/6421) conv3d kW and kH×kW LDS reuse on gfx950 (Qwen)
- [#5993](https://github.com/ROCm/aiter/pull/5993) `hc_mix` kernel for Qwen3.8 hyper-connections
- [#6416](https://github.com/ROCm/aiter/pull/6416) `fused_indexed_gated_residual` for diffusion transformers
- [#6674](https://github.com/ROCm/aiter/pull/6674) `fused_gemm_a16w16_mul_add` for the DiT gated residual
- [#6038](https://github.com/ROCm/aiter/pull/6038) fused gated RMSNorm + MXFP4 quant
- [#6634](https://github.com/ROCm/aiter/pull/6634) `gluon_fused_qk_norm` for gfx1250
- [#6501](https://github.com/ROCm/aiter/pull/6501) tune `fused_bmm_rope_kv_cache`, add bench and configs
- [#6287](https://github.com/ROCm/aiter/pull/6287) benchmark, config and tuning for `fused_qk_concat`
- [#6451](https://github.com/ROCm/aiter/pull/6451) paged MQA logits kernels read (B, next_n) context lengths
- [#6504](https://github.com/ROCm/aiter/pull/6504) Triton Conv2D padding primitives
- [#6000](https://github.com/ROCm/aiter/pull/6000) Gemma (1 + w) weights in fused AR+RMSNorm+MXFP4 quant
- [#6570](https://github.com/ROCm/aiter/pull/6570) support up to TP64 in all-gather
- [#6607](https://github.com/ROCm/aiter/pull/6607) gfx1250 192x256 no-ps A4W4 and dispatch fix
- [#3993](https://github.com/ROCm/aiter/pull/3993) wire `is_causal` through `mla_decode_fwd`
- [#6161](https://github.com/ROCm/aiter/pull/6161) `x_EQ_x` config matcher for unified attention
- [#6633](https://github.com/ROCm/aiter/pull/6633) remove the bad `mla_decode.py` op
- [#6640](https://github.com/ROCm/aiter/pull/6640) round custom all-reduce BF16 stores to nearest even
- [#6821](https://github.com/ROCm/aiter/pull/6821) (open) `fused_norm_rope_att_rope_cast` kernel
- [#6822](https://github.com/ROCm/aiter/pull/6822) (open) MHA v4 sparsified online attention (gfx950)
- [#6670](https://github.com/ROCm/aiter/pull/6670) (open) fused QSA sparse decode for gfx950
- [#6743](https://github.com/ROCm/aiter/pull/6743) (open) HipKittens H32 sparse MLA for gfx950
- [#6669](https://github.com/ROCm/aiter/pull/6669) (open) gfx11 flash attention forward in FlyDSL
- [#6764](https://github.com/ROCm/aiter/pull/6764) (open) non-causal mode for multi-token PA decode
- [#6660](https://github.com/ROCm/aiter/pull/6660) (open) per-token FP8 KV and split-K verify in gfx1250 unified attention
- [#6830](https://github.com/ROCm/aiter/pull/6830) (open) eight-row FP8 MQA logits path for gfx950
- [#6672](https://github.com/ROCm/aiter/pull/6672) (open) BF16 state storage in gfx950 KDA
- [#6745](https://github.com/ROCm/aiter/pull/6745) (open) fused compress attention in Gluon
- [#6678](https://github.com/ROCm/aiter/pull/6678) (open) `fused_reduce_add_rmsnorm`
- [#6779](https://github.com/ROCm/aiter/pull/6779) (open) `fused_qkv_split_qk_norm_rope_cache`: MRoPE, shuffle KV layout, optional outputs
- [#6808](https://github.com/ROCm/aiter/pull/6808) (open) optional pre-quant `k_out_unquantized` under FP8 KV cache
- [#6734](https://github.com/ROCm/aiter/pull/6734) (open) fuse a 32-point Hadamard rotation into MXFP4 per-1x32 quant
- [#6710](https://github.com/ROCm/aiter/pull/6710) (open) `fused_layernorm_indexed_adaln` for diffusion
- [#6721](https://github.com/ROCm/aiter/pull/6721) (open) `group_norm` with optional temb add and activation
- [#6707](https://github.com/ROCm/aiter/pull/6707) (open) bias and `gate_first` option for `gemm_a16w16_gated`
- [#6815](https://github.com/ROCm/aiter/pull/6815) (open) opt-in prefix-budget metadata planner for PA
- [#6832](https://github.com/ROCm/aiter/pull/6832) (open) reuse query quantization in fused FP8 BMM
- [#6727](https://github.com/ROCm/aiter/pull/6727) (open) split-K A8W8 BMM with fused reduce-quant
- [#6698](https://github.com/ROCm/aiter/pull/6698) (open) BMM and inverse-RoPE quant kernels for gfx1250
- [#6662](https://github.com/ROCm/aiter/pull/6662) (open) gfx1250 implicit-GEMM conv3d
- [#6810](https://github.com/ROCm/aiter/pull/6810) (open) FlyDSL FCA
- [#6754](https://github.com/ROCm/aiter/pull/6754) (open) Muse Spark MoE GEMM with shuffled weights
- [#6767](https://github.com/ROCm/aiter/pull/6767) (open) gfx1250-strict architecture plumbing

</details>

<details>
<summary>MoE & quantization (28)</summary>

- [#6544](https://github.com/ROCm/aiter/pull/6544) fused MoE tune for DSR1 FP4 TP8
- [#6622](https://github.com/ROCm/aiter/pull/6622) v41 TP2 MoE config for shared-expert fusion at 8k/16k input
- [#6611](https://github.com/ROCm/aiter/pull/6611) fuse MoE stage-2 input quant into the stage-1 epilogue (DSV4.1Flash)
- [#6610](https://github.com/ROCm/aiter/pull/6610) bound the a8w4 MoE activation quant to the live token count
- [#6693](https://github.com/ROCm/aiter/pull/6693) Qwen3.8-Flash-Next FP8 fused-MoE configs for gfx942
- [#6593](https://github.com/ROCm/aiter/pull/6593) Muse Spark Open MXFP4 FMoE tuning for gfx950
- [#6681](https://github.com/ROCm/aiter/pull/6681) Qwen3-235B FP8 EP: drop token=1,2 rows that lose to the CK default
- [#6468](https://github.com/ROCm/aiter/pull/6468) Qwen3.8 TP=8 MXFP4 MoE aux kernel codegen
- [#6379](https://github.com/ROCm/aiter/pull/6379) typed APIs in MoE routing and MX quantization
- [#6688](https://github.com/ROCm/aiter/pull/6688) gfx942 a16w4 MoE tiles for gpt-oss decode on Triton 3.8
- [#6742](https://github.com/ROCm/aiter/pull/6742) (open) HipKittens block-FP8 MoE for gfx950
- [#6696](https://github.com/ROCm/aiter/pull/6696) (open) Blockscale MXFP8 OPUS GEMM
- [#6778](https://github.com/ROCm/aiter/pull/6778) (open) `gemm_a16w4` INT4 weight-only GEMM for GPTQ/AWQ
- [#6828](https://github.com/ROCm/aiter/pull/6828) (open) gfx950 4-wave INT8 bpreshuffle GEMM
- [#6824](https://github.com/ROCm/aiter/pull/6824) (open) 1x32 bmm bpreshuffle in OPUS
- [#6825](https://github.com/ROCm/aiter/pull/6825) (open) gfx950 MXFP6 GEMM tuning candidates
- [#6823](https://github.com/ROCm/aiter/pull/6823) (open) gfx1250 A8W4 MoE row-bucketed configs for gpt-oss
- [#6768](https://github.com/ROCm/aiter/pull/6768) (open) Kimi-K3 TP8 gfx1250 grouped-MoE tuning
- [#6817](https://github.com/ROCm/aiter/pull/6817) (open) Muse Spark Open MXFP4 FMoE rows
- [#6820](https://github.com/ROCm/aiter/pull/6820) (open) Kimi-K3 gfx950 BF16 tuned rows
- [#6708](https://github.com/ROCm/aiter/pull/6708) (open) Qwen3.8-Flash-Next MXFP4 a4w4 MoE tuning
- [#6694](https://github.com/ROCm/aiter/pull/6694) (open) align persistent workgroup count for fmoe kernels that remap across XCDs
- [#6691](https://github.com/ROCm/aiter/pull/6691) (open) check model_dim for gfx950 FP8 blockscale 1-stage MoE
- [#6736](https://github.com/ROCm/aiter/pull/6736) (open) use K=128 for gfx950 FP8 stage2 when 256 does not divide inter_dim
- [#6766](https://github.com/ROCm/aiter/pull/6766) (open) launch persistent ASM fused_moe kernels with total_tgs workgroups
- [#6720](https://github.com/ROCm/aiter/pull/6720) (open) split path above 8192 columns for `fused_dynamic_mx_quant_moe_sort`
- [#6786](https://github.com/ROCm/aiter/pull/6786) (open) `out_zeroed` skips the split-K memset in a8w8 blockscale ASM
- [#6728](https://github.com/ROCm/aiter/pull/6728) (open) rotating buffers and `do_bench_aiter_triton` for MoE benchmarks

</details>

<details>
<summary>Hardware & arch tuning configs (30)</summary>

- [#6664](https://github.com/ROCm/aiter/pull/6664) merge of the PR 5770 conflicts with Triton tuning review (large cross-arch update)
- [#6687](https://github.com/ROCm/aiter/pull/6687) gfx1250 Gluon GEMMs for DeepSeek-R1
- [#6725](https://github.com/ROCm/aiter/pull/6725) gfx1250 Gluon GEMMs for Kimi-K2 Thinking
- [#6717](https://github.com/ROCm/aiter/pull/6717) gfx1250 MiniMax-M3 PTPC GEMMs
- [#6695](https://github.com/ROCm/aiter/pull/6695) gluon a16w16 configs for dsv4.1 MoE router and KV compressor shapes
- [#6769](https://github.com/ROCm/aiter/pull/6769) gfx950 a8w8 bpreshuffle and BF16 GEMM for Qwen3.8 Flash Next
- [#6653](https://github.com/ROCm/aiter/pull/6653) gfx1250 MXFP4 GEMMs for Llama3 70B
- [#6652](https://github.com/ROCm/aiter/pull/6652) gfx1250 MXFP4 GEMMs for Llama3 8B
- [#6654](https://github.com/ROCm/aiter/pull/6654) gfx1250 MXFP4 GEMMs for Llama3 405B
- [#6650](https://github.com/ROCm/aiter/pull/6650) gfx1250 a16w16 GEMMs for Llama4 Maverick
- [#6649](https://github.com/ROCm/aiter/pull/6649) gfx1250 a16w16 GEMMs for Qwen3-235B-A22B
- [#6726](https://github.com/ROCm/aiter/pull/6726) DSR1 input projection tuning
- [#6744](https://github.com/ROCm/aiter/pull/6744) sweep NUM_BUFFERS and kernel_type for gfx1250 persistent a16w16 and blockscale preshuffle
- [#6749](https://github.com/ROCm/aiter/pull/6749) A4W4 prefill MMA groups 8/8 and B TDM TH 1
- [#6680](https://github.com/ROCm/aiter/pull/6680) retune gfx950 a16w16 N=2880 K=4096 for gpt-oss-20b o_proj decode
- [#6061](https://github.com/ROCm/aiter/pull/6061) gfx950 GEMM configs for N=K=2048
- [#5961](https://github.com/ROCm/aiter/pull/5961) gfx1101 (RDNA3) a16w16 configs
- [#6671](https://github.com/ROCm/aiter/pull/6671) gfx1151 a16w16 DEFAULT.json
- [#6374](https://github.com/ROCm/aiter/pull/6374) gfx1200/gfx1201 Triton MHA configs
- [#6763](https://github.com/ROCm/aiter/pull/6763) (open) Kimi-K3 TP8 gfx1250 GEMM tune
- [#6741](https://github.com/ROCm/aiter/pull/6741) (open) retune gfx950 preshuffled AFP4WFP4 decode for Llama-3.3-70B MXFP4
- [#6683](https://github.com/ROCm/aiter/pull/6683) (open) gfx950 preshuffled AFP4WFP4 for DeepSeek MXFP4 TP8 dense shapes
- [#6711](https://github.com/ROCm/aiter/pull/6711) (open) gfx950 BF16 GEMMs for Qwen3.8-Flash-Next (TP1, MTP 3)
- [#6713](https://github.com/ROCm/aiter/pull/6713) (open) gfx950 a8w8 bpreshuffle for Qwen3.8-Flash-Next PTPC
- [#6757](https://github.com/ROCm/aiter/pull/6757) (open) gfx942 a8w8 blockscale configs for Qwen3 shapes
- [#6759](https://github.com/ROCm/aiter/pull/6759) (open) retune gfx950 ops that regressed with Triton 3.8
- [#6740](https://github.com/ROCm/aiter/pull/6740) (open) gfx950 a16w16 M_LEQ_8 VGPR-spill fix
- [#6780](https://github.com/ROCm/aiter/pull/6780) (open) gfx950 BF16 batched GEMM for Kimi-K2.6
- [#6771](https://github.com/ROCm/aiter/pull/6771) (open) gfx1100 A16W16 for Llama-3-8B and Qwen3
- [#6784](https://github.com/ROCm/aiter/pull/6784) (open) gfx1250 PA decode tuning

</details>

<details>
<summary>Bugfixes (42)</summary>

- [#6639](https://github.com/ROCm/aiter/pull/6639) wrong results in gfx942 FP8 persistent/blockscale fused-MoE dispatch
- [#6606](https://github.com/ROCm/aiter/pull/6606) gfx950 GQA16 MTP softmax initialization
- [#6750](https://github.com/ROCm/aiter/pull/6750) disable spurious [-64,64] output clamp in MLA and preserve FP32 denominator
- [#5320](https://github.com/ROCm/aiter/pull/5320) int32 overflow in the paged MQA logits preshuffle K/scale load offset
- [#6629](https://github.com/ROCm/aiter/pull/6629) gfx1250 gemm_a16w16 dropping output rows past 2**31 bytes
- [#4687](https://github.com/ROCm/aiter/pull/4687) fp8_mqa_logits epilogue store masks for cu_start != 0
- [#6679](https://github.com/ROCm/aiter/pull/6679) gfx1250 Gluon a8w8 blockscale NUM_BUFFERS config key
- [#6456](https://github.com/ROCm/aiter/pull/6456) zero-pad XQ to padded weight K for a8w8 bpreshuffle
- [#6428](https://github.com/ROCm/aiter/pull/6428) NaN dq in Triton MHA backward on very negative logits
- [#6095](https://github.com/ROCm/aiter/pull/6095) Triton topk with -inf rows
- [#6138](https://github.com/ROCm/aiter/pull/6138) scale gfx942 Sage probabilities before FP8 conversion
- [#5642](https://github.com/ROCm/aiter/pull/5642) scale FP8 softmax probabilities in paged_attention_ragged
- [#6641](https://github.com/ROCm/aiter/pull/6641) `scaled_silu_and_mul` device-side scale, FP8 saturation and row bounds
- [#6700](https://github.com/ROCm/aiter/pull/6700) replay biased interleaved MoE callers
- [#6556](https://github.com/ROCm/aiter/pull/6556) MegaMoE dispatch source-indexed payload fix
- [#6395](https://github.com/ROCm/aiter/pull/6395) write grouped MoE tuning results back in place
- [#6398](https://github.com/ROCm/aiter/pull/6398) bind `load_hip_runtime` to the already-loaded HIP runtime
- [#6738](https://github.com/ROCm/aiter/pull/6738) import aiter with no visible GPU
- [#5991](https://github.com/ROCm/aiter/pull/5991) missing extension module names in pretune builds
- [#6327](https://github.com/ROCm/aiter/pull/6327) MI300A support and XCD count fix
- [#6616](https://github.com/ROCm/aiter/pull/6616) `-DONLY_FAV3=0` quoting in the backward JIT build
- [#5687](https://github.com/ROCm/aiter/pull/5687) Flash Attention CI failures
- [#6592](https://github.com/ROCm/aiter/pull/6592) `topk_sigmoid` pybind conversion fix, later reverted by [#6811](https://github.com/ROCm/aiter/pull/6811)
- [#6811](https://github.com/ROCm/aiter/pull/6811) revert of [#6592](https://github.com/ROCm/aiter/pull/6592)
- [#6699](https://github.com/ROCm/aiter/pull/6699) (open) gfx1250 fused all-reduce+RMSNorm and LL block size
- [#6756](https://github.com/ROCm/aiter/pull/6756) (open) gfx1250 LL all-reduce
- [#6819](https://github.com/ROCm/aiter/pull/6819) (open) keep CUDA-graph buffer registration in step across ranks in CustomAR
- [#6755](https://github.com/ROCm/aiter/pull/6755) (open) mask stale V rows past the sequence end in gfx950 Gluon unified attention
- [#6661](https://github.com/ROCm/aiter/pull/6661) (open) wrong output when the packed KV cache is 2-4 GiB
- [#6798](https://github.com/ROCm/aiter/pull/6798) (open) paged_attention_ll4mi query-head offset for GQA ratios above 16
- [#6760](https://github.com/ROCm/aiter/pull/6760) (open) preserve virtual sinks in single-query batch prefill
- [#6703](https://github.com/ROCm/aiter/pull/6703) (open) MLA metadata v1.0 tail
- [#6663](https://github.com/ROCm/aiter/pull/6663) (open) dropped K tail and bias column offset in grouped MoE TDM GEMM
- [#6677](https://github.com/ROCm/aiter/pull/6677) (open) bound per-tensor quant vector tails
- [#6761](https://github.com/ROCm/aiter/pull/6761) (open) topk_select must not evict default end-index rows captured by graphs
- [#6758](https://github.com/ROCm/aiter/pull/6758) (open) int64 for Triton split-K partial offsets
- [#6712](https://github.com/ROCm/aiter/pull/6712) (open) FlyDSL A16W16 AOT semaphore dtype
- [#6704](https://github.com/ROCm/aiter/pull/6704) (open) FlyDSL a8w8 tuner on gfx942 without async copy
- [#6719](https://github.com/ROCm/aiter/pull/6719) (open) gfx1250 MXFP4 quant, RMSNorm and gemm_afp4wfp4 failures on Triton 3.8
- [#6751](https://github.com/ROCm/aiter/pull/6751) (open) `fused_qk_norm_rope_group_quant`
- [#6773](https://github.com/ROCm/aiter/pull/6773) (open) compat shim for `get_scaled_upcast_fp4_scale_layout` on upstream Triton
- [#6705](https://github.com/ROCm/aiter/pull/6705) (open) Triton fp8 dtype fix

</details>

<details>
<summary>Numerics & rounding (4)</summary>

- [#6748](https://github.com/ROCm/aiter/pull/6748) (open) round CK FMHA bf16 conversions to nearest instead of truncating
- [#6665](https://github.com/ROCm/aiter/pull/6665) (open) round CK-Tile a8w8 GEMM bf16 outputs to nearest even on gfx942
- [#6706](https://github.com/ROCm/aiter/pull/6706) (open) fit gfx1250 grouped GEMM k-tile to K, refuse non-dividing tiles
- [#6692](https://github.com/ROCm/aiter/pull/6692) (open) FMoE tuner uses all sources for shapes FlyDSL v2 cannot tune

</details>

<details>
<summary>Refactors (7)</summary>

- [#6380](https://github.com/ROCm/aiter/pull/6380) simplify FlyDSL kernel APIs and remove redundant wrappers
- [#5164](https://github.com/ROCm/aiter/pull/5164) simplify AITER compiler worker fan-out
- [#6252](https://github.com/ROCm/aiter/pull/6252) FlyDSL TDM new interface
- [#6716](https://github.com/ROCm/aiter/pull/6716) revert of [#6252](https://github.com/ROCm/aiter/pull/6252)
- [#6718](https://github.com/ROCm/aiter/pull/6718) (open) TDM new interface v2
- [#6809](https://github.com/ROCm/aiter/pull/6809) (open) clean up `test_pa_decode_gluon`
- [#6347](https://github.com/ROCm/aiter/pull/6347) consistent parser arg in benchmarks

</details>

<details>
<summary>Tests & benchmarks (22)</summary>

- [#6690](https://github.com/ROCm/aiter/pull/6690) `bench_pa_decode` reports real KV bandwidth and times with CUDA graphs
- [#6747](https://github.com/ROCm/aiter/pull/6747) stop `test_extend_attention` changing the default dtype
- [#6709](https://github.com/ROCm/aiter/pull/6709) (open) FlyDSL test improvements
- [#6715](https://github.com/ROCm/aiter/pull/6715) (open) Vernier micro-benchmark improvements
- [#6814](https://github.com/ROCm/aiter/pull/6814) (open) benchmark scripts for Semi AgentX and model_config override fix
- [#6816](https://github.com/ROCm/aiter/pull/6816) (open) MoE EP bench with no-mega support on gfx1250
- [#6682](https://github.com/ROCm/aiter/pull/6682) (open) rotating buffers and `do_bench_aiter_triton` for quant, CE and transpose
- [#6684](https://github.com/ROCm/aiter/pull/6684) (open) same for DeepSeek kernels
- [#6813](https://github.com/ROCm/aiter/pull/6813) (open) common rotating-buffer helpers
- [#6783](https://github.com/ROCm/aiter/pull/6783) (open) fix cuda assignments in UTs
- [#6797](https://github.com/ROCm/aiter/pull/6797) (open) fix UT leaks
- [#6795](https://github.com/ROCm/aiter/pull/6795) (open) fix UT leaks
- [#6796](https://github.com/ROCm/aiter/pull/6796) (open) fix MHA UT
- [#6737](https://github.com/ROCm/aiter/pull/6737) (open) Flash Attention PR followup
- [#6714](https://github.com/ROCm/aiter/pull/6714) (open) do not specialize `attn_fwd` on max seqlen
- [#6730](https://github.com/ROCm/aiter/pull/6730) (open) assert num_stages=2 for 3D unified attention on gfx1250
- [#6782](https://github.com/ROCm/aiter/pull/6782) (open) `is_sw_emulated_fp8_avail()` for gfx11, enabling the Triton MHA fp8 path
- [#6739](https://github.com/ROCm/aiter/pull/6739) (open) import `aiter.ops.triton.quant` with no visible GPU
- [#6676](https://github.com/ROCm/aiter/pull/6676) (open) gfx1151 gemm_a16w16 rounding before activation to avoid spills
- [#6770](https://github.com/ROCm/aiter/pull/6770) (open) fav3_sage RDNA3 support
- [#6772](https://github.com/ROCm/aiter/pull/6772) (open) gfx1100 RMSNorm large-M/small-N config
- [#6797](https://github.com/ROCm/aiter/pull/6797) and [#6795](https://github.com/ROCm/aiter/pull/6795) overlap on UT leak cleanup

</details>

<details>
<summary>CI & build (6)</summary>

- [#6657](https://github.com/ROCm/aiter/pull/6657) auto-update split test times
- [#6722](https://github.com/ROCm/aiter/pull/6722) Triton board: label-driven
- [#6364](https://github.com/ROCm/aiter/pull/6364) relax Standard Test Results reporting
- [#6812](https://github.com/ROCm/aiter/pull/6812) (open) include tests/ in test sharding
- [#6666](https://github.com/ROCm/aiter/pull/6666) (open) update ASM code objects
- [#6826](https://github.com/ROCm/aiter/pull/6826) (open) restore gfx950 PA 2TG vector loads

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (AITER.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: f9cf8c093e3edb2282e9a03dcb93db27dcded011d9c55502ce58be21361e0a19 -->
