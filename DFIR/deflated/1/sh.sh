#!/bin/bash

# Step 1: Create complex project structure
mkdir -p zipchallenge/{src/public/{css,js},config,secrets,.hidden}
cd zipchallenge

# Initialize git repo with multiple branches
git init
git checkout -b dev

# Create initial valid files
echo "# Secure Archive Challenge" > README.md
cat > src/public/index.html <<EOF
<!DOCTYPE html>
<html>
<head>
    <title>Secure Archive</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <!-- Flag part 1/4: MED{Z1P_ -->
    <h1>Secure Archive System</h1>
    <script src="js/loader.js"></script>
</body>
</html>
EOF

echo "body { color: #333; }" > src/public/css/style.css
echo "// Loader script" > src/public/js/loader.js

# Create fake secret files
echo "DB_PASSWORD=not_the_flag" > config/.env
echo "SECRET_KEY=st1ll_n0t_th3_fl4g" > secrets/keys.txt

git add . && git commit -m "Initial project setup"

# Step 2: Add multiple flag fragments in different locations
# Fragment 1: In HTML comment
sed -i 's/<!-- Flag part 1\/4: MED{Z1P_/<!-- Flag part 1\/4: MED{Z1P_CR4CK_/' src/public/index.html
git add . && git commit -m "Update header styling"

# Fragment 2: In binary blob
echo -n "D3FL4T3D" > .hidden/part2.bin
git add .hidden/part2.bin && git commit -m "Add binary assets"

# Fragment 3: In deleted file
echo "M4ST3R}" > src/temp_flag.txt
git add src/temp_flag.txt && git commit -m "Add temporary configuration"
git rm src/temp_flag.txt && git commit -m "Remove temporary files"

# Fragment 4: In commit message itself
echo "API_ENDPOINT=https://github.com/aarab-ayoub/wildfly" >> config/.env
git add . && git commit -m "Update config - FlagPart: _VULNERABLE_"

# Step 3: Add misdirection commits
for i in {1..5}; do
    echo "FAKE_FLAG_${i}=decoy$RANDOM" >> secrets/keys.txt
    git add . && git commit -m "Update security keys"
done

# Step 4: Create encrypted archive with multiple protection layers
ZIP_PASSWORD="easy_password"  # Set an easy password
zip -r -e --password "$ZIP_PASSWORD" \
    -9 ../challenge.zip . 

# Step 5: Create multiple hint files with red herrings
# echo "ref: refs/heads/main" > plain_git_head.txt
# echo "Password hint: Check commit on 2020-02-28" > fake_hint.txt  # Fixed invalid date
# echo "FLAG_PART=CR4CK" > .env.example