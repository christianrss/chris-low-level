using System.Threading.Channels;
namespace Chris.ChannelLab;
public static class Pipeline {
    public static async Task<(int checksum,int count)> RunAsync(int count,int capacity) {
        // PEDAGOGY-SOLUTION: D7-DN-CHANNEL
        var channel=Channel.CreateBounded<int>(new BoundedChannelOptions(capacity){FullMode=BoundedChannelFullMode.Wait,SingleWriter=true,SingleReader=true});
        int checksum=0, seen=0;
        // PEDAGOGY-SOLUTION: D7-DN-PRODUCER
        var producer=Task.Run(async ()=>{
            try { for(int i=0;i<count;i++) await channel.Writer.WriteAsync(i); }
            finally { channel.Writer.Complete(); }
        });
        // PEDAGOGY-SOLUTION: D7-DN-CONSUMER
        var consumer=Task.Run(async ()=>{
            await foreach(var item in channel.Reader.ReadAllAsync()){ checksum+=item; seen++; await Task.Yield(); }
        });
        await Task.WhenAll(producer,consumer);
        return (checksum,seen);
    }
}
