package com.expedia.ecs.service;

import io.github.jopenlibs.vault.Vault;
import io.github.jopenlibs.vault.VaultConfig;
import io.github.jopenlibs.vault.response.LogicalResponse;
import org.springframework.stereotype.Service;

/**
 * Direct Vault Access Service for HCOM/EWE/VRBO
 * This needs to be updated to use EG Vault
 */
@Service
public class VaultService {

    private static final String HCOM_VAULT_ENDPOINT = "https://vault.hcom.expedia.com";
    private static final String EWE_VAULT_ENDPOINT = "https://vault.ewe.expedia.com";
    private static final String VRBO_VAULT_ENDPOINT = "https://vault.vrbo.expedia.com";

    /**
     * HCOM Vault access pattern
     */
    public String getSecretFromHcomVault(String secretPath) {
        // HCOM Vault pattern
        VaultConfig config = new VaultConfig()
            .address(HCOM_VAULT_ENDPOINT)
            .build();
        
        Vault vault = new Vault(config);
        LogicalResponse response = vault.logical().read(secretPath);
        return response.getData().get("value");
    }

    /**
     * EWE Vault access pattern
     */
    public String getSecretFromEweVault(String secretPath) {
        // EWE Vault pattern
        VaultConfig config = new VaultConfig()
            .address(EWE_VAULT_ENDPOINT)
            .build();
        
        Vault vault = new Vault(config);
        LogicalResponse response = vault.logical().read(secretPath);
        return response.getData().get("value");
    }

    /**
     * VRBO Vault access pattern
     */
    public String getSecretFromVrboVault(String secretPath) {
        // VRBO Vault pattern
        VaultConfig config = new VaultConfig()
            .address(VRBO_VAULT_ENDPOINT)
            .build();
        
        Vault vault = new Vault(config);
        LogicalResponse response = vault.logical().read(secretPath);
        return response.getData().get("value");
    }
}

