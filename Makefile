all: clean download-apps build-apps test

test:
	nosetests tests

download-apps: clean
	cd apps/src; \
	    curl -LO http://developer.apple.com/library/ios/samplecode/UICatalog/UICatalog.zip; \
	    unzip UICatalog.zip; \
	    rm UICatalog.zip

build-apps:
	cd apps/src/UICatalog; \
	    xcodebuild -sdk iphonesimulator6.1 -arch i386; \
	    mv build/Release-iphonesimulator/UICatalog.app ../../built/

clean:
	rm -rf apps/built
	rm -rf apps/src/UICatalog
