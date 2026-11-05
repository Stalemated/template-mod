package com.stalemated.templatemod.loader;

//? if neoforge {
/*import com.stalemated.templatemod.TemplateMod;
import com.stalemated.templatemod.TemplateModClient;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;

@Mod(TemplateMod.MOD_ID)
public final class TemplateModNeoForge {
    public TemplateModNeoForge(IEventBus modBus, Dist dist) {
        TemplateMod.init();
        if (dist == Dist.CLIENT) {
            TemplateModClient.init();
        }
    }
}
*///?}
