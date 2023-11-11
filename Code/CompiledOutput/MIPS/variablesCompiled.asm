.globl main
.data:
	print1:	.asciiz	"Beginning Gurt Program...\n"
	x:	.word	0
	y:	.word	0
	z:	.word	0
	print5:	.asciiz	"Enter a value for x: "
	print6:	.asciiz	"Enter a value for y: "
	print7:	.asciiz	"Enter a value for z: "
	print8:	.asciiz	"In order, you entered the numbers:\n"
	print9:	.asciiz	"\tx: "
	print11:	.asciiz	"\n\ty: "
	print13:	.asciiz	"\n\tz: "
	print15:	.asciiz	"\n"
	print16:	.asciiz	"In reverse order, you entered the numbers:\n"
	print17:	.asciiz	"\tz: "
	print19:	.asciiz	"\n\ty: "
	print21:	.asciiz	"\n\tx: "
	print23:	.asciiz	"\n"
	print25:	.asciiz	"The operation z = x + y is computed as follows:\n"
	print26:	.asciiz	"z"
	print27:	.asciiz	" = "
	print29:	.asciiz	" + "
	print31:	.asciiz	"\n"
	print32:	.asciiz	"The result of the operation is:\n"
	print33:	.asciiz	"z = "
	
.text:
main:
	li $v0, 4
	la $a0, print1
	syscall
	li $v0, 4
	la $a0, print5
	syscall
	li $v0, 5
	syscall
	sw $v0, x
	li $v0, 4
	la $a0, print6
	syscall
	li $v0, 5
	syscall
	sw $v0, y
	li $v0, 4
	la $a0, print7
	syscall
	li $v0, 5
	syscall
	sw $v0, z
	li $v0, 4
	la $a0, print8
	syscall
	li $v0, 4
	la $a0, print9
	syscall
	li $v0, 1
	lw $a0, x
	syscall
	li $v0, 4
	la $a0, print11
	syscall
	li $v0, 1
	lw $a0, y
	syscall
	li $v0, 4
	la $a0, print13
	syscall
	li $v0, 1
	lw $a0, z
	syscall
	li $v0, 4
	la $a0, print15
	syscall
	li $v0, 4
	la $a0, print16
	syscall
	li $v0, 4
	la $a0, print17
	syscall
	li $v0, 1
	lw $a0, z
	syscall
	li $v0, 4
	la $a0, print19
	syscall
	li $v0, 1
	lw $a0, y
	syscall
	li $v0, 4
	la $a0, print21
	syscall
	li $v0, 1
	lw $a0, x
	syscall
	li $v0, 4
	la $a0, print23
	syscall
	lw $t0, z
	lw $t1, x
	lw $t2, y
	add $t0, $t1, $t2
	sw $t0, z
	li $v0, 4
	la $a0, print25
	syscall
	li $v0, 4
	la $a0, print26
	syscall
	li $v0, 4
	la $a0, print27
	syscall
	li $v0, 1
	lw $a0, x
	syscall
	li $v0, 4
	la $a0, print29
	syscall
	li $v0, 1
	lw $a0, y
	syscall
	li $v0, 4
	la $a0, print31
	syscall
	li $v0, 4
	la $a0, print32
	syscall
	li $v0, 4
	la $a0, print33
	syscall
	li $v0, 1
	lw $a0, z
	syscall
	li $v0, 10
	syscall