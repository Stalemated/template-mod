package com.stalemated.templatemod.config;

import com.stalemated.lib.compat.yacl.SLibTesting;
import com.stalemated.lib.config.InMemoryConfigManager;
import org.junit.jupiter.api.Test;

import java.nio.file.Path;

class TemplateModConfigScreenTest {
    @Test
    void theConfigScreenBuilds() throws Exception {
        SLibTesting.assertScreenBuilds(
                TemplateModConfigScreen.builder(null, new InMemoryConfigManager<>(new TemplateModConfig(), TemplateModConfig::new, null)),
                Path.of(TemplateModConfigScreenTest.class.getResource("/assets/template_mod/lang/en_us.json").toURI())
        );
    }
}
