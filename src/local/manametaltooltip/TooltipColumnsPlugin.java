package local.manametaltooltip;

import cpw.mods.fml.relauncher.FMLLaunchHandler;
import cpw.mods.fml.relauncher.IFMLLoadingPlugin;
import cpw.mods.fml.relauncher.Side;
import java.util.Map;

@IFMLLoadingPlugin.Name("ManaMetal Tooltip Columns")
@IFMLLoadingPlugin.MCVersion("1.7.10")
@IFMLLoadingPlugin.SortingIndex(1001)
@IFMLLoadingPlugin.TransformerExclusions({"local.manametaltooltip.asm."})
public final class TooltipColumnsPlugin implements IFMLLoadingPlugin {
    public String[] getASMTransformerClass() {
        return FMLLaunchHandler.side() == Side.CLIENT
                ? new String[] {"local.manametaltooltip.asm.TooltipTransformer"} : new String[0];
    }
    public String getModContainerClass() { return null; }
    public String getSetupClass() { return null; }
    public String getAccessTransformerClass() { return null; }
    public void injectData(Map<String, Object> data) { }
}
