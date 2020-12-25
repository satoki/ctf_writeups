.intel_syntax noprefix
.globl check_flag, key, answer

/*
mov a, b
	a = b

add a, b
	a = a + b

xor a, b
	a = a ^ b

lea a, b
	a = &b

SIZE PTR [a]
	aからSIZE分読みこむ
	QWORD: 8byte
	DWORD: 4byte
	WORD: 2byte
	BYTE: 1bytes

jmp label
	goto label

cmp a, b
j** label
	jne: if (a != b) goto label
	jle: if (a <= b) goto label

rax, rbx, cl, dl
	レジスタ。一時変数だと思っても問題ないが、このアーキテクチャではいくつか変数には役割がある
	rdi: 第一引数
	rax: 返り値
	rbp: スタックの一番下を指すポインタ
	その他rspなどにも役割は存在するが、今回は関係ないので割愛する。

スタック:
	ローカル変数に割り当てられるメモリのこと。
	+------+
	+ 0x14 +
	+------+ <= rbp - 4
	+ 0x13 +
	+------+ <= rbp - 3
	+ 0x12 +
	+------+ <= rbp - 2
	+ 0x11 +
	+------+ <= rbp - 1
	+ 0x10 +
	+------+ <= rbp
	BYTE PTR [rbp - 4]は 0x13、
	DWORD PTR [rbp - 4]は 0x10111213　に当たる。
*/

# Let's reversing!

key:
	.string ";,Z,.(7TWT2$jAU2#YLZ!QE^,(D h;H\t"

answer:
	.string "CAn_U_Re4d_A55emBly?L3t's_tRY_it"

check_flag:
	# 関数の開始処理 (おまじない)
	push rbp
	mov rbp, rsp

	mov QWORD PTR [rbp - 0x8], rdi
	mov QWORD PTR [rbp - 0x10], 0

	.for_start:
		mov rax, QWORD PTR [rbp - 0x8]
		mov rbx, QWORD PTR [rbp - 0x10]
		mov cl, BYTE PTR [rax + rbx]
		
		lea rax, key
		mov rbx, QWORD PTR [rbp - 0x10]
		mov dl, BYTE PTR [rax + rbx]

		xor cl, dl

		lea rax, answer
		mov rbx, QWORD PTR [rbp - 0x10]
		mov dl, BYTE PTR [rax + rbx]
		
		cmp cl, dl
		jne .if_false

		.if_true:
			jmp .if_end

		.if_false:
			mov eax, 0
			jmp .function_end

		.if_end:

	.for_end:
	add QWORD PTR [rbp - 0x10], 1
	cmp QWORD PTR [rbp - 0x10], 32
	jle .for_start

	mov eax, 1
	.function_end:

	# 関数の終了処理 (おまじない)
	leave
	ret
