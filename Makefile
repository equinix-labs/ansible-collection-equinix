SHELL := /bin/bash
COLLECTIONS_PATH ?= ~/.ansible/collections
DOCS_PATH ?= docs
VERSION_FILE=version
COLLECTION_VERSION := $(shell cat ${VERSION_FILE})

TEST_ARGS := -v ${test_target}
INTEGRATION_CONFIG := tests/integration/integration_config.yml
METAL_TEST_METRO ?= sv

clean:
	rm -f *.tar.gz && rm -rf galaxy.yml

build: clean 
	python scripts/render_galaxy.py $(COLLECTION_VERSION) && ansible-galaxy collection build

publish: build
	@if test "$(GALAXY_TOKEN)" = ""; then \
	  echo "GALAXY_TOKEN must be set"; \
	  exit 1; \
	fi
	ansible-galaxy collection publish --token $(GALAXY_TOKEN) *.tar.gz

install: build
	ansible-galaxy collection install *.tar.gz --force -p $(COLLECTIONS_PATH)

deps:
	pip install -r requirements.txt -r requirements-dev.txt

lint:
	pylint plugins

	mypy plugins/modules
	mypy plugins/inventory

.PHONY: docs
docs: inject-module-docs
	rm -rf $(DOCS_PATH)/modules $(DOCS_PATH)/inventory
	mkdir -p $(DOCS_PATH)/modules $(DOCS_PATH)/inventory
	DOCS_PATH=$(DOCS_PATH) ./scripts/specdoc_generate.sh
	python scripts/render_readme.py ${COLLECTION_VERSION}
	ansible-doc-extractor --template=template/module.rst.j2 $(DOCS_PATH)/inventory plugins/inventory/metal_device.py

.PHONY: inject-module-docs
inject-module-docs:
	DOCS_PATH=$(DOCS_PATH) ./scripts/specdoc_inject.sh

.PHONY: remove-module-docs
remove-module-docs:
	DOCS_PATH=$(DOCS_PATH) ./scripts/specdoc_remove.sh

test: integration-test

testall:
	./scripts/test_all.sh

integration-test: create-integration-config
	ansible-test integration $(TEST_ARGS)

create-integration-config:
ifneq ("${METAL_API_TOKEN}", "")
	@echo "metal_api_token: ${METAL_API_TOKEN}" > $(INTEGRATION_CONFIG);
else
	echo "METAL_API_TOKEN must be set"; \
	exit 1;
endif
	echo "metal_ua_prefix: E2E" >> $(INTEGRATION_CONFIG)
	echo "metal_test_metro: $(METAL_TEST_METRO)" >> $(INTEGRATION_CONFIG)

ifneq ("${METAL_HARDWARE_RESERVATION_ID}", "")
	echo "metal_hardware_reservation_id: ${METAL_HARDWARE_RESERVATION_ID}" >> $(INTEGRATION_CONFIG)
endif
ifneq ("${METAL_HARDWARE_RESERVATION_PROJECT_ID}", "")
	echo "metal_hardware_reservation_project_id: ${METAL_HARDWARE_RESERVATION_PROJECT_ID}" >> $(INTEGRATION_CONFIG)
endif

