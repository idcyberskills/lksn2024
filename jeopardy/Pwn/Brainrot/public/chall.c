#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <seccomp.h>

void sandbox(){
	scmp_filter_ctx ctx;
	ctx = seccomp_init(SCMP_ACT_KILL);
	seccomp_rule_add(ctx, SCMP_ACT_ALLOW, __NR_read, 0);
	seccomp_rule_add(ctx, SCMP_ACT_ALLOW, __NR_write, 0);
	seccomp_rule_add(ctx, SCMP_ACT_ALLOW, __NR_open, 0);
	seccomp_load(ctx);
}

char func[0x100];

void main(){
        mprotect((void *)((unsigned long)func & ~0xfff), 0x1000, 7);
	sandbox();
	printf("send me your gyatttt mewing sigma rizzz fanumtax skibidi alpha beta gamma delta epsilon zeta theta omega\n");	
	printf("and btw the flag is in /flagdottieksti.txt\n");
	printf("so you can just print it\n");
	read(0, func, sizeof(func));
	((void (*)())func)();
}


__attribute__((constructor))
void init(void){
	setbuf(stdin, NULL);
	setbuf(stdout, NULL);
}
