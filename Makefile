PROJECT = "AAP-Infrastructure"
TAG=`cat VERSION`

current-version:
	@echo "Current version is $(TAG)"

release:
	cut-branch merge-release push-release current-version

cut-branch:
	git checkout -b release/$(TAG) develop

merge-release:
	git checkout master && \
		git merge --no-ff release/$(TAG) && \
		git tag -a "v$(TAG)" -m "v$(TAG)" && \
		git checkout develop && \
		git merge --no-ff release/$(TAG) && \
		git branch -d release/$(TAG)

push-release:
	git push origin master && \
		git push origin develop && \
		git push origin --tags && \
		git push origin :release/$(TAG)