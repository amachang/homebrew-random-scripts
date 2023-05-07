#!/usr/sbin/dtrace -s

#pragma D option quiet

struct ioinfo_t {
    int initialized;
    string execname;
    pid_t pid;
    uint64_t start_ns;
};

struct ioinfo_t ioinfo_map[int64_t];

dtrace:::BEGIN
{
    printf("Sampling... Hit Ctrl-C to end.\n");
}

io:::start
{
    this->ioinfo = ioinfo_map[arg0];

    this->ioinfo.execname = execname;
    this->ioinfo.pid = pid;
    this->ioinfo.start_ns = timestamp;
    this->ioinfo.initialized = 1;

    ioinfo_map[arg0] = this->ioinfo;
}

io:::done / ioinfo_map[arg0].initialized == 1 /
{
    this->ioinfo = ioinfo_map[arg0];

    this->device = args[1]->dev_instance;

    @io_time[this->ioinfo.execname, this->ioinfo.pid, this->device] = sum(timestamp - this->ioinfo.start_ns);
    this->ioinfo.initialized = 0;
    this->ioinfo.execname = "";
    this->ioinfo.pid = 0;
    this->ioinfo.start_ns = 0;

    ioinfo_map[arg0] = this->ioinfo;
}

profile:::tick-5sec
{
    printf("===== IO Occupation in 5 Sec ============================\n");
    printf("%-32s %-6s %3s %10s\n", "Command", "Pid", "Device", "Nano Sec");
    printf("---------------------------------------------------------\n");
    printa("%-32s %-6d %6d %@10d\n", @io_time);
    printf("---------------------------------------------------------\n");
    printf("\n");
    trunc(@io_time);
}

