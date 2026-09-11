namespace Chris.JitLab;
public abstract class Animal { public abstract string Speak(); }
public class Dog : Animal { public override string Speak() => "woof"; }
public static class CallSite {
    public static string Dispatch(Animal a) {
        // TODO [D9-DN-VIRT]
        throw new NotImplementedException();
    }
    public static string DevirtDog(Dog d) {
        // TODO [D9-DN-DEVIRT]
        throw new NotImplementedException();
    }
    public static bool IsExactDog(Animal a) {
        // TODO [D9-DN-TYPE]
        throw new NotImplementedException();
    }
}
