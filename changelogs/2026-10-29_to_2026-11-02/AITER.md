# AITER: PR digest (2026-10-29 to 2026-11-02)

_58 merged, 133 newly opened - source ROCm/AITER, generated 2026-11-02T00:26:08Z_

## TL;DR
- **DeepSeek (V4/V4.1) got the most attention**, followed by Kimi-K3, MiniMax-M3 and Qwen3.5/3.8. Work was mostly gfx1250 (66 PRs) and gfx950 bring-up: Mega-MHC kernels, FP8/FP4 GEMM and MoE tuning, and an MXFP8 sparse MLA kernel (opened).
- **MoE and fusion were the biggest perf theme.** Merged: MegaMoE on gfx1250 with a mori combine path, HERD routing for GPT-OSS, and MI308 decode tuning. Opened: MegaMoEV2 over SDMA, a small-token MegaMoE TP path, and FP8 MoE at any multiple-of-8 intermediate size.
- **Communication fusion landed.** Custom allreduce now fuses the residual add with row-selective RMSNorm (merged). A gfx1250 all-reduce fusion, a gemm+allreduce+RMSNorm Gluon kernel and 6-rank allreduce fixes are open.
- **Attention is moving to Gluon, FlyDSL and ASM.** A productized Gluon MHA for gfx950 merged. Open work covers gfx950 MLA/MQA FP8/FP4 prefill kernels, mHC decode speedups and FlyDSL paged-attention decode.
- **Direction:** a large share of the 133 new PRs are tuning configs and CPU-overhead trims (stream and tensor allocation, dispatcher caching). CI got gating and ccache work.

## Most important PRs
**[#6430](https://github.com/ROCm/aiter/pull/6430) MegaMoE gfx1250 (merged)**: Adds stage1/stage2 switches, a mori combine path and the current mori EPv2 to the fused MoE pipeline across Gluon, FlyDSL and Triton. This is the largest change of the window (+4.3k lines). `[#7200](https://github.com/ROCm/aiter/pull/7200)` is its internal CI mirror.

**[#6270](https://github.com/ROCm/aiter/pull/6270) Custom allreduce with fused residual add and row-selective RMSNorm (merged)**: Folds the residual add and RMSNorm into the allreduce kernel, which removes separate norm launches in TP decode.

**[#5153](https://github.com/ROCm/aiter/pull/5153) Gluon MHA for gfx950 (merged)**: Productizes the gfx950 Gluon MHA kernel from the tutorials into a production attention path.

**[#7131](https://github.com/ROCm/aiter/pull/7131) Mega-MHC kernels for DeepSeek-V4.1 (merged)**: Adds gfx1250 HIP kernels with fused MXFP8 and row-major scales for DeepSeek-V4.1's mHC block.

**[#5970](https://github.com/ROCm/aiter/pull/5970) hipBLASLt grouped GEMM backend for SonicMoE (merged)**: Adds an opt-in hipBLASLt grouped GEMM path for MoE expert GEMMs.

## More changes by area

<details>
<summary>Performance (14)</summary>

- [#7181](https://github.com/ROCm/aiter/pull/7181) (open) gfx950 mHC decode speedup using Gram statistics
- [#7151](https://github.com/ROCm/aiter/pull/7151) (open) gfx950 mHC row finalization and packed prefill fusion
- [#7137](https://github.com/ROCm/aiter/pull/7137) (open) stable and deterministic topk_select sampling mode on gfx950
- [#7152](https://github.com/ROCm/aiter/pull/7152) (open) several rows per block in dynamic_per_token_scaled_quant for cols <= 2048
- [#7279](https://github.com/ROCm/aiter/pull/7279) (open) act_mul_and_mxfp4_quant rounds to E2M1 with the gfx950 instruction
- [#7231](https://github.com/ROCm/aiter/pull/7231) (open) tune the act_mul_and_fp8_group_quant launch on gfx942
- [#7210](https://github.com/ROCm/aiter/pull/7210) (open) cut fused MoE dispatcher keyword-matching overhead
- [#7217](https://github.com/ROCm/aiter/pull/7217) (open) avoid dummy dispatch tensors in inference collectives
- [#7219](https://github.com/ROCm/aiter/pull/7219) (open) avoid torch Stream construction across grouped MoE launches
- [#7248](https://github.com/ROCm/aiter/pull/7248) (open) avoid empty Tensor construction for omitted MoE operands
- [#7261](https://github.com/ROCm/aiter/pull/7261) (open) cache grouped MoE integer config parsing
- [#7262](https://github.com/ROCm/aiter/pull/7262) (open) avoid allocating an unread MoE quantizer placeholder
- [#7172](https://github.com/ROCm/aiter/pull/7172) (open) skip unused intermediate allocation in fused stage-1 quantization
- [#7211](https://github.com/ROCm/aiter/pull/7211) (open) specialize Triton GEMM grid and split loops

</details>

<details>
<summary>Kernels & attention (45)</summary>

- [#6745](https://github.com/ROCm/aiter/pull/6745) fused compress attention in Gluon (gfx1250)
- [#6635](https://github.com/ROCm/aiter/pull/6635) rotating buffers and do_bench_aiter_triton support for fused kernels
- [#6815](https://github.com/ROCm/aiter/pull/6815) opt-in prefix-budget metadata planner for PA
- [#7087](https://github.com/ROCm/aiter/pull/7087) mla_reduce_v1 handles 12 heads at head dim 128
- [#7115](https://github.com/ROCm/aiter/pull/7115) split-K tuning for mhc_fused_post_pre_delayed_rmsnorm decode
- [#6594](https://github.com/ROCm/aiter/pull/6594) route short sliding-window queries to the gfx950 split grid
- [#6999](https://github.com/ROCm/aiter/pull/6999) unified attention 2D passes num_seqs and block_table_stride at runtime
- [#6996](https://github.com/ROCm/aiter/pull/6996) gfx1250 mha bwd d192/d128 kernel integration
- [#6645](https://github.com/ROCm/aiter/pull/6645) query XCC count through HIP and share it with FlyDSL PA
- [#5925](https://github.com/ROCm/aiter/pull/5925) stop serving-time recompiles of _prefill_row_plan_kernel
- [#7253](https://github.com/ROCm/aiter/pull/7253) unified_attention 2D bounds gathered page ids
- [#6404](https://github.com/ROCm/aiter/pull/6404) hidden 6144 support in INT4 QuickReduce + RMSNorm epilogue
- [#7155](https://github.com/ROCm/aiter/pull/7155) captured gfx1250 inputs read in place on custom_ar IPC
- [#7124](https://github.com/ROCm/aiter/pull/7124) (open) gfx950 MLA v4.1 a8w4 prefill kernels for NVFP4 prefix KV
- [#7276](https://github.com/ROCm/aiter/pull/7276) (open) gfx1250 MXFP8 sparse MLA kernel for DSV4.1 with FP8 KV cache
- [#7184](https://github.com/ROCm/aiter/pull/7184) (open) gfx950 paged FP8 MQA logits
- [#7183](https://github.com/ROCm/aiter/pull/7183) (open) gfx950 prefill FP8 MQA logits
- [#7128](https://github.com/ROCm/aiter/pull/7128) (open) OPUS FP4 MQA writer and query scale layouts
- [#7173](https://github.com/ROCm/aiter/pull/7173) (open) gfx950 hd256 MXFP4 MHA v4 with per-batch seqlens_k
- [#7192](https://github.com/ROCm/aiter/pull/7192) (open) MHA v4 production on gfx950
- [#7186](https://github.com/ROCm/aiter/pull/7186) (open) Gluon MHA for gfx1250
- [#7187](https://github.com/ROCm/aiter/pull/7187) (open) MLA for gfx1250
- [#7244](https://github.com/ROCm/aiter/pull/7244) (open) non-causal unified_attention
- [#7242](https://github.com/ROCm/aiter/pull/7242) (open) read DeepSeek-V4.1 KV records in sparse MLA
- [#7171](https://github.com/ROCm/aiter/pull/7171) (open) fused bf16 BMM + cat + FP8 quant + head pad for MLA decode
- [#7125](https://github.com/ROCm/aiter/pull/7125) (open) balance the gfx950 XCD-lane decode planner on skewed KV lengths
- [#7245](https://github.com/ROCm/aiter/pull/7245) (open) native 96-head FP8 MLA decode at qlen 7-8 under round-robin CP
- [#7239](https://github.com/ROCm/aiter/pull/7239) (open) pipelining for fused GDN decode kernel
- [#7225](https://github.com/ROCm/aiter/pull/7225) (open) KDA packed decode accepts the fused conv1d weight
- [#7206](https://github.com/ROCm/aiter/pull/7206) (open) expose can_use_flydsl_pa_decode
- [#7205](https://github.com/ROCm/aiter/pull/7205) (open) PA planner batch and capacity as runtime values
- [#7197](https://github.com/ROCm/aiter/pull/7197) (open) peel the last KV tile in pa_decode
- [#7199](https://github.com/ROCm/aiter/pull/7199) (open) head-256 FP8 pa_decode takes three M-tiles
- [#7269](https://github.com/ROCm/aiter/pull/7269) (open) gfx1250 PA wave query tiles two through four
- [#7214](https://github.com/ROCm/aiter/pull/7214) (open) per-tensor fp8 descales for gfx1250 FMHA a8w8
- [#7215](https://github.com/ROCm/aiter/pull/7215) (open) gfx950 sliding-window fmha_bwd kernels
- [#7160](https://github.com/ROCm/aiter/pull/7160) (open) gfx1250 mha bwd hd64 and hd128 border mask
- [#7277](https://github.com/ROCm/aiter/pull/7277) (open) MHA fp8 prefill runs the fp16 kernel on archs with emulated fp8
- [#7232](https://github.com/ROCm/aiter/pull/7232) (open) out_dtype on the Triton MHA forward
- [#7280](https://github.com/ROCm/aiter/pull/7280) (open) flash_attn_varlen_fp8_pertensor_func writes into the caller's output
- [#7120](https://github.com/ROCm/aiter/pull/7120) (open) fused Q/K Gemma RMSNorm + MRoPE + KV cache write for Qwen3.5
- [#7133](https://github.com/ROCm/aiter/pull/7133) (open) write the asm MLA decode KV layout from fused_qk_rope_cat_and_cache_mla
- [#7256](https://github.com/ROCm/aiter/pull/7256) (open) fused_rmsnorm_add row kernel and gemma_norm
- [#7167](https://github.com/ROCm/aiter/pull/7167) (open) fused SiTU-and-mul Triton kernel
- [#7174](https://github.com/ROCm/aiter/pull/7174) (open) bench_sage routes hd256 to the MXFP4 producers
- [#7265](https://github.com/ROCm/aiter/pull/7265) (open) gfx1250 LL all-gather up to 4 MiB per rank

</details>

<details>
<summary>MoE & quantization (31)</summary>

- [#6527](https://github.com/ROCm/aiter/pull/6527) HERD on gfx1250 and a fused HERD selector for GPT-OSS
- [#5973](https://github.com/ROCm/aiter/pull/5973) MI308 MoE decoding optimization (3/3)
- [#6219](https://github.com/ROCm/aiter/pull/6219) moe_gemm_a8w8 fnuz FP8 and MXFP8 on gfx942
- [#6557](https://github.com/ROCm/aiter/pull/6557) tune DeepSeek-R1 FP4 MoE tiles for high-batch decode on gfx1250
- [#6437](https://github.com/ROCm/aiter/pull/6437) gemm_a8w8_bpreshuffle_out for caller-owned bf16 outputs
- [#7095](https://github.com/ROCm/aiter/pull/7095) generalize gfx1250 TP MoE route histograms for wide expert sets
- [#7113](https://github.com/ROCm/aiter/pull/7113) register-resident top-p sampling for the top-k-first path
- [#7264](https://github.com/ROCm/aiter/pull/7264) (open) optimize MegaMoE TP for small token counts
- [#7196](https://github.com/ROCm/aiter/pull/7196) (open) MegaMoEV2 with SDMA Stage2 and combine, 8-wave GEMM2
- [#7127](https://github.com/ROCm/aiter/pull/7127) (open) tune DSv4.1 EP8 A8W4 MegaMoE
- [#7129](https://github.com/ROCm/aiter/pull/7129) (open) FP8 MoE at any multiple-of-8 intermediate size without HBM padding
- [#7153](https://github.com/ROCm/aiter/pull/7153) (open) a16w4 gfx942 opt-in fp8 MFMA mode
- [#7135](https://github.com/ROCm/aiter/pull/7135) (open) public two-stage fused_moe_stage1/stage2 API
- [#7188](https://github.com/ROCm/aiter/pull/7188) (open) tune gfx1250 A4W4 MoE prefill TDM GEMM
- [#7146](https://github.com/ROCm/aiter/pull/7146) (open) gfx1250 FlyDSL prefill work
- [#7252](https://github.com/ROCm/aiter/pull/7252) (open) fewer scan barriers in gfx1250 fused TP routing
- [#7275](https://github.com/ROCm/aiter/pull/7275) (open) wave32 ballots for small persistent expert lookup
- [#7223](https://github.com/ROCm/aiter/pull/7223) (open) keep FP4 quant K-splits before selecting compact scales
- [#7134](https://github.com/ROCm/aiter/pull/7134) (open) multi-phase MoE sorting for gfx950 E=128..255 decode at M>=17
- [#7178](https://github.com/ROCm/aiter/pull/7178) (open) batched mxfp8 GEMM with fused quant epilogue
- [#7238](https://github.com/ROCm/aiter/pull/7238) (open) WIP FlyDSL a8w8 256x256 persistent kernel
- [#7122](https://github.com/ROCm/aiter/pull/7122) (open) gfx1250 gemm_a16w16 + all-reduce + RMSNorm for 4 ranks
- [#7212](https://github.com/ROCm/aiter/pull/7212) (open) fused all-reduce RMSNorm for MiniMax-M3 shapes
- [#7157](https://github.com/ROCm/aiter/pull/7157) (open) all-reduce fusion with FlyDSL
- [#7228](https://github.com/ROCm/aiter/pull/7228) (open) fused a16w16 GEMM with separate tile and split-K per output
- [#7258](https://github.com/ROCm/aiter/pull/7258) (open) QuickAllReduce INT4 E5M2 group scale
- [#7272](https://github.com/ROCm/aiter/pull/7272) (open) optimize DSv4 flash performance
- [#7123](https://github.com/ROCm/aiter/pull/7123) (open) route rmsnorm and pertoken_quant through the kernel provider interface
- [#7139](https://github.com/ROCm/aiter/pull/7139) (open) relu2 for legacy ck_gemm_moe_2stages
- [#7243](https://github.com/ROCm/aiter/pull/7243) (open) reuse preshuffle_on ck2stages modules, add PREBUILD_KERNELS=4
- [#7271](https://github.com/ROCm/aiter/pull/7271) (open) cache HERD host launches and retire legacy BMM entry points

</details>

<details>
<summary>Model support & tuning configs (50)</summary>

- [#6573](https://github.com/ROCm/aiter/pull/6573) gfx1250 Gluon GEMM configs for Kimi-K2 TP8
- [#7162](https://github.com/ROCm/aiter/pull/7162) gfx950 Llama blockscale GEMM configs
- [#6410](https://github.com/ROCm/aiter/pull/6410) Kimi-K3 gfx950 A8W8 bpreshuffle configs
- [#6535](https://github.com/ROCm/aiter/pull/6535) MI300A GLM-5.3 FP8 blockscale GEMM and fused MoE configs
- [#7142](https://github.com/ROCm/aiter/pull/7142) Kimi-K3 DSpark PTPC/blockscale and f_b_proj GEMM rows
- [#7070](https://github.com/ROCm/aiter/pull/7070) gfx1250 FlyDSL bf16 GEMM rows for Kimi-K2 TP8
- [#6820](https://github.com/ROCm/aiter/pull/6820) Kimi-K3 gfx950 BF16 rows for the MoE front and DSpark QKV
- [#7018](https://github.com/ROCm/aiter/pull/7018) DeepSeek-V4 FP8 GEMM tuning on gfx1250
- [#5821](https://github.com/ROCm/aiter/pull/5821) DeepSeek-V4 EP8 a8w4 MXFP4 fused-MoE rows for gfx950
- [#7177](https://github.com/ROCm/aiter/pull/7177) Qwen3.5 c128 host attention
- [#7105](https://github.com/ROCm/aiter/pull/7105) per-CU-count config trees
- [#6922](https://github.com/ROCm/aiter/pull/6922) tuning scripts write the largest bucket as "any"
- [#7218](https://github.com/ROCm/aiter/pull/7218) (open) MI350P tuned GEMM and fused-MoE configs
- [#7254](https://github.com/ROCm/aiter/pull/7254) (open) MI350P Gemma-4-31B FP8-block blockscale GEMMs
- [#7235](https://github.com/ROCm/aiter/pull/7235) (open) Mistral Large 4 gfx950 tables
- [#7247](https://github.com/ROCm/aiter/pull/7247) (open) DeepSeek-V4.1-Flash BF16 and MX32 FP8 GEMM rows
- [#7234](https://github.com/ROCm/aiter/pull/7234) (open) DeepSeek-V4.1-Flash dense FP8 tiles for intermediate M
- [#7246](https://github.com/ROCm/aiter/pull/7246) (open) DSv4.1 BF16 LM-head and router GEMMs
- [#7221](https://github.com/ROCm/aiter/pull/7221) (open) DSv4 flash MoE config for gfx1250
- [#7209](https://github.com/ROCm/aiter/pull/7209) (open) MiniMax-M3 TP4 BF16, indexer-CP QKV and MoE token 1024
- [#7170](https://github.com/ROCm/aiter/pull/7170) (open) MiniMax-M3-EAGLE3.1 BF16 GEMMs
- [#7230](https://github.com/ROCm/aiter/pull/7230) (open) MiniMax-M3 MXFP4 MoE TP8 configs
- [#7259](https://github.com/ROCm/aiter/pull/7259) (open) MiniMax-M3 MoE rows (TP2 a4w4 prefill, TP8 a16w4)
- [#7138](https://github.com/ROCm/aiter/pull/7138) (open) Kimi-K3 gfx1250 gemm_a4w4
- [#7169](https://github.com/ROCm/aiter/pull/7169) (open) Kimi-K3 gfx950 BF16 GEMM rows
- [#7189](https://github.com/ROCm/aiter/pull/7189) (open) K3 tuned values on gfx1250
- [#7198](https://github.com/ROCm/aiter/pull/7198) (open) Qwen3.5-397B mxfp4 lm_head, FP8 projection and MoE rows
- [#7233](https://github.com/ROCm/aiter/pull/7233) (open) Qwen3.8-27B gfx942 a8w8 blockscale rows
- [#7204](https://github.com/ROCm/aiter/pull/7204) (open) Qwen3.8-Flash-Next TP4 prefill BF16 on MI308X
- [#7267](https://github.com/ROCm/aiter/pull/7267) (open) Qwen3.5-35B-A3B a4w4 MoE at EP4
- [#7224](https://github.com/ROCm/aiter/pull/7224) (open) Beam FP8 fused MoE configs for gfx950
- [#7249](https://github.com/ROCm/aiter/pull/7249) (open) gfx1151 gemm_a16w4 configs
- [#7260](https://github.com/ROCm/aiter/pull/7260) (open) gfx1150 gemm_a16w4 configs
- [#7154](https://github.com/ROCm/aiter/pull/7154) (open) gfx1150 Conv3D configs
- [#7282](https://github.com/ROCm/aiter/pull/7282) (open) gfx1150 gemm_a8w8_preshuffled int8 configs
- [#7270](https://github.com/ROCm/aiter/pull/7270) (open) gfx1151 gemm_a8w8_preshuffled int8 tuning (1.24x vs main)
- [#7257](https://github.com/ROCm/aiter/pull/7257) (open) reuse gfx1151 attn_fwd config on gfx1150
- [#7255](https://github.com/ROCm/aiter/pull/7255) (open) num_stages 2 for the head-512 fp8 prefill tile
- [#7121](https://github.com/ROCm/aiter/pull/7121) (open) rotating-buffer pool accepts exclude list and tensor containers

</details>

<details>
<summary>Hardware & arch (3)</summary>

- [#7159](https://github.com/ROCm/aiter/pull/7159) OPUS CU lookup compatibility and gfx1250 kernel queries
- [#7185](https://github.com/ROCm/aiter/pull/7185) (open) OPUS falls back to regular COs when A0 strict is unsupported
- [#7103](https://github.com/ROCm/aiter/pull/7103) ignore-tti-inline-compatible flag for the ROCm 10.1 LLVM compiler

</details>

<details>
<summary>Bugfixes (30)</summary>

- [#7147](https://github.com/ROCm/aiter/pull/7147) fix PA decode scaling and merge alignment
- [#7092](https://github.com/ROCm/aiter/pull/7092) pa_decode zeroes V rows past the context before PV
- [#6519](https://github.com/ROCm/aiter/pull/6519) bound scatter-reduce staging reads in MoE
- [#7016](https://github.com/ROCm/aiter/pull/7016) preserve typed E8M0 scales in gfx1250 MoE routing
- [#7130](https://github.com/ROCm/aiter/pull/7130) fix gfx1250 HERD decode routing and extend past 512 experts
- [#7042](https://github.com/ROCm/aiter/pull/7042) sync both wave groups in the gfx950 A16W16 HTI GEMM
- [#7047](https://github.com/ROCm/aiter/pull/7047) mask OOB e8m0 scales in batched_gemm_afp4wfp4
- [#7110](https://github.com/ROCm/aiter/pull/7110) num_local_tokens fix in ASM kernels
- [#7074](https://github.com/ROCm/aiter/pull/7074) bench_mega_moe kernel table fix and --fused_shared_experts
- [#7101](https://github.com/ROCm/aiter/pull/7101) accept generic torch.Stream in torch_to_c_types
- [#7097](https://github.com/ROCm/aiter/pull/7097) temporarily disable a MHAv4 rotated fp8 test on gfx942
- [#7119](https://github.com/ROCm/aiter/pull/7119) (open) gfx1250 GEMM output offset overflow
- [#7136](https://github.com/ROCm/aiter/pull/7136) (open) CK-Tile MXFP4 MoE stage1 split-k for unaligned K
- [#7126](https://github.com/ROCm/aiter/pull/7126) (open) never share scratch buffers whose zero fill was graph-recorded
- [#7149](https://github.com/ROCm/aiter/pull/7149) (open) 6-rank custom collectives
- [#7222](https://github.com/ROCm/aiter/pull/7222) (open) guard dropped expert IDs in MoE route and remap
- [#7251](https://github.com/ROCm/aiter/pull/7251) (open) honor omitted valid-route counts in EP routing
- [#7263](https://github.com/ROCm/aiter/pull/7263) (open) legal buffer access widths for vec8 MoE gather-reduce
- [#7266](https://github.com/ROCm/aiter/pull/7266) (open) ep_sort_routing barrier before the last-CTA ticket
- [#7202](https://github.com/ROCm/aiter/pull/7202) (open) gfx1250 a8w4 MoE decode output store from registers
- [#7203](https://github.com/ROCm/aiter/pull/7203) (open) gfx1250 unified attention decode output from registers
- [#7201](https://github.com/ROCm/aiter/pull/7201) (open) zero V rows past the sequence end in gfx1250 Gluon attention
- [#7182](https://github.com/ROCm/aiter/pull/7182) (open) MLA decode merges only the splits written by gfx950 bf16 gqa32 stage 1
- [#7220](https://github.com/ROCm/aiter/pull/7220) (open) _fold_seqlen_indptr perf error
- [#7281](https://github.com/ROCm/aiter/pull/7281) (open) OOB e8m0 scale mask in fused_gemm_afp4wfp4 variants
- [#7236](https://github.com/ROCm/aiter/pull/7236) (open) OOB scale loads in batched_gemm_afp4wfp4
- [#7148](https://github.com/ROCm/aiter/pull/7148) (open) zombie lock holder in FileBaton
- [#7283](https://github.com/ROCm/aiter/pull/7283) (open) reject non-contiguous mixes and out in mhc_post
- [#7179](https://github.com/ROCm/aiter/pull/7179) (open) clear error when hipconfig is missing
- [#7164](https://github.com/ROCm/aiter/pull/7164) (open) ambiguous HIP error helper lookup in CK-free shim
- [#7161](https://github.com/ROCm/aiter/pull/7161) (open) include HIP bfloat16 header in MoE sorting
- [#7268](https://github.com/ROCm/aiter/pull/7268) (open) ep_sort_routing grid size at run time

</details>

<details>
<summary>Refactors (2)</summary>

- [#7191](https://github.com/ROCm/aiter/pull/7191) rename gfx1250 TDM kernel prefix from a8w4 to mxfp4
- [#7213](https://github.com/ROCm/aiter/pull/7213) (open) make_tdm_atom becomes make_tiled_tdm_atom

</details>

<details>
<summary>CI & build (16)</summary>

- [#7003](https://github.com/ROCm/aiter/pull/7003) shadow PR self-review gate
- [#7163](https://github.com/ROCm/aiter/pull/7163) drop Test Gate requirement for CI-only changes
- [#7156](https://github.com/ROCm/aiter/pull/7156) route self-review writes through the aiter-bot PAT
- [#7029](https://github.com/ROCm/aiter/pull/7029) Triton nightly test
- [#6975](https://github.com/ROCm/aiter/pull/6975) bump FlyDSL pin to 0.4.1
- [#7208](https://github.com/ROCm/aiter/pull/7208) package aiter skills as a Claude Code plugin
- [#7207](https://github.com/ROCm/aiter/pull/7207) (open) create-pr skill
- [#7165](https://github.com/ROCm/aiter/pull/7165) (open) select op_tests from the PR diff (dry run)
- [#7166](https://github.com/ROCm/aiter/pull/7166) (open) narrow two op_test shape sweeps on PR runs
- [#7180](https://github.com/ROCm/aiter/pull/7180) (open) ccache across builds (2h16m to about 6m)
- [#7229](https://github.com/ROCm/aiter/pull/7229) (open) run selected Triton tests on each merge to main
- [#7250](https://github.com/ROCm/aiter/pull/7250) (open) update triton-nightly-watchers
- [#7226](https://github.com/ROCm/aiter/pull/7226) (open) FlyDSL review guidance
- [#7227](https://github.com/ROCm/aiter/pull/7227) (open) review-pr FlyDSL checks D13/D14
- [#7195](https://github.com/ROCm/aiter/pull/7195) (open) manual gfx1201 DevLab smoke test (do not merge)
- [#7200](https://github.com/ROCm/aiter/pull/7200) (open) MegaMoE gfx1250 internal CI mirror, see [#6430](https://github.com/ROCm/aiter/pull/6430)

</details>

<details>
<summary>Docs (1)</summary>

- [#7216](https://github.com/ROCm/aiter/pull/7216) (open) persist FlyDSL kernel caches across containers

</details>

<details>
<summary>Other (6)</summary>

- [#7137](https://github.com/ROCm/aiter/pull/7137) is listed under Performance
- [#7274](https://github.com/ROCm/aiter/pull/7274) (open) honor the requested grouped MoE activation format in tests
- [#7157](https://github.com/ROCm/aiter/pull/7157) is listed under MoE & quantization
- [#7123](https://github.com/ROCm/aiter/pull/7123) is listed under MoE & quantization
- [#7220](https://github.com/ROCm/aiter/pull/7220) is listed under Bugfixes
- [#7264](https://github.com/ROCm/aiter/pull/7264) is listed under MoE & quantization

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (AITER.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 024e69fd3fc307a2625fb72e511cb311b297eb3e0cc285b12c0eb5679e14a3ad -->
