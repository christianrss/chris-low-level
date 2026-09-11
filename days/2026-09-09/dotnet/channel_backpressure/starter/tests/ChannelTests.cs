using System.Threading.Tasks;
using Chris.ChannelLab;
using Xunit;
public class ChannelTests {
    [Fact]
    public async Task Run() {
        // PEDAGOGY-TEST: D7-DN-CHANNEL
        // PEDAGOGY-TEST: D7-DN-PRODUCER
        // PEDAGOGY-TEST: D7-DN-CONSUMER
        var (sum, n) = await Pipeline.RunAsync(5, 2);
        Assert.Equal(10, sum);
        Assert.Equal(5, n);
    }
}
