import { WORKSPACE_DATA_DIR } from '$env/static/private';
import fs from 'node:fs';
import path from 'node:path';

/** @param {string} workspaceId */
function getWorkspaceDir(workspaceId) {
  const workspaceDir = path.join(WORKSPACE_DATA_DIR, workspaceId);
  if (!fs.existsSync(workspaceDir)) {
    fs.mkdirSync(workspaceDir);
    addFile(workspaceId, 'main.sus');
  }
  return workspaceDir;
}

/** @param {string} workspaceId */
export function deleteWorkspace(workspaceId) {
  const workspaceDir = path.join(WORKSPACE_DATA_DIR, workspaceId);
  if (fs.existsSync(workspaceDir)) {
    fs.rmdirSync(workspaceDir, { recursive: true });
  }
}

/**
 * @param {string} workspaceId
 */
export function workspaceFiles(workspaceId) {
  const workspaceDir = getWorkspaceDir(workspaceId);
  return fs.readdirSync(workspaceDir);
}

/**
 * @param {string} workspaceId
 * @param {string} filename
 */
function getFilePath(workspaceId, filename) {
  const workspaceDir = getWorkspaceDir(workspaceId);
  return path.join(workspaceDir, filename);
}

/**
 * @param {string} workspaceId
 * @param {string} filename
 */
export function addFile(workspaceId, filename) {
  const filePath = getFilePath(workspaceId, filename);
  if (!fs.existsSync(filePath)) {
    fs.writeFileSync(filePath, '');
  }
}

/**
 * @param {string} workspaceId
 * @param {string} filename
 */
export function removeFile(workspaceId, filename) {
  const filePath = getFilePath(workspaceId, filename);
  if (fs.existsSync(filePath)) {
    fs.unlinkSync(filePath);
  }
}

/**
 * @param {string} workspaceId
 * @param {string} filename
 */
export function fileContents(workspaceId, filename) {
  const filePath = getFilePath(workspaceId, filename);
  return fs.readFileSync(filePath);
}

/**
 * @param {string} workspaceId
 * @param {string} filename
 * @param {string} content
 */
export function saveFile(workspaceId, filename, content) {
  const filePath = getFilePath(workspaceId, filename);
  fs.writeFileSync(filePath, content);
}
