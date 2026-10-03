package local.manametaltooltip;

import cpw.mods.fml.common.Mod;
import cpw.mods.fml.common.event.FMLPreInitializationEvent;
import net.minecraftforge.common.config.Configuration;

@Mod(modid="manametaltooltipcolumns", name="ManaMetal Tooltip Columns", version="1.0.0",
        acceptedMinecraftVersions="[1.7.10]", acceptableRemoteVersions="*",
        dependencies="after:manametalmod")
public final class TooltipColumnsMod {
    public static boolean enabled = true;
    public static int maxColumnWidth = 240;
    public static int screenMargin = 6;
    public static int columnGap = 8;

    @Mod.EventHandler public void preInit(FMLPreInitializationEvent event) {
        Configuration config = new Configuration(event.getSuggestedConfigurationFile());
        enabled = config.getBoolean("enabled", "general", true, "Split overflowing ManaMetal item tooltips.");
        maxColumnWidth = config.getInt("maxColumnWidth", "general", 240, 100, 600,
                "Maximum width per column, in scaled GUI pixels. Long lines wrap with colors preserved.");
        screenMargin = config.getInt("screenMargin", "general", 6, 4, 24, "Space between tooltip and screen edges.");
        columnGap = config.getInt("columnGap", "general", 8, 4, 24, "Space between tooltip panels.");
        if (config.hasChanged()) config.save();
    }
}
