提交代码到 GitHub，按以下步骤执行：

1. **检查状态**：运行 git status 和 git diff，确认有哪些变更。
2. **检查敏感文件**：确认 keys.yaml 等敏感文件没有被误加入暂存区。如果有，警告并中止。
3. **暂存文件**：将相关变更文件加入暂存区（不要用 git add -A，逐个添加）。
4. **生成 commit message**：根据变更内容生成简洁的中文 commit message，格式为：类型(范围): 描述。类型包括 feat/fix/refactor/docs/chore 等。
5. **提交**：执行 git commit。
6. **推送**：执行 git push。如果远程分支不存在，使用 git push -u origin <branch>。

注意：
- 每一步执行前先确认上一步成功。
- 如果没有任何变更，直接告知用户，不要执行空提交。
- 用中文输出执行过程。
