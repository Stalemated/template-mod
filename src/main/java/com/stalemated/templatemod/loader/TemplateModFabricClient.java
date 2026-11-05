package com.stalemated.templatemod.loader;

//? if fabric {
import com.stalemated.templatemod.TemplateModClient;
import net.fabricmc.api.ClientModInitializer;

public final class TemplateModFabricClient implements ClientModInitializer {
    @Override
    public void onInitializeClient() {
        TemplateModClient.init();
    }
}
//?}
