using Chris.JitLab;
using Xunit;
public class JitTests {
    [Fact]
    public void Virt() {
        // PEDAGOGY-TEST: D9-DN-VIRT
        // PEDAGOGY-TEST: D9-DN-DEVIRT
        // PEDAGOGY-TEST: D9-DN-TYPE
        Animal a = new Dog();
        Assert.Equal("woof", CallSite.Dispatch(a));
        Assert.Equal("woof", CallSite.DevirtDog((Dog)a));
        Assert.True(CallSite.IsExactDog(a));
    }
}
