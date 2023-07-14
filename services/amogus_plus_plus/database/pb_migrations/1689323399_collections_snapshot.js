migrate((db) => {
  const snapshot = [
    {
      "id": "_pb_users_auth_",
      "created": "2023-06-29 10:16:32.961Z",
      "updated": "2023-06-29 10:22:11.507Z",
      "name": "users",
      "type": "auth",
      "system": false,
      "schema": [],
      "indexes": [],
      "listRule": "id = @request.auth.id",
      "viewRule": "id = @request.auth.id",
      "createRule": "",
      "updateRule": "id = @request.auth.id",
      "deleteRule": "id = @request.auth.id",
      "options": {
        "allowEmailAuth": false,
        "allowOAuth2Auth": false,
        "allowUsernameAuth": true,
        "exceptEmailDomains": null,
        "manageRule": null,
        "minPasswordLength": 5,
        "onlyEmailDomains": null,
        "requireEmail": false
      }
    },
    {
      "id": "5b62gswbvx6alk6",
      "created": "2023-07-10 06:39:35.697Z",
      "updated": "2023-07-14 08:16:36.380Z",
      "name": "workspaces",
      "type": "base",
      "system": false,
      "schema": [
        {
          "system": false,
          "id": "vwxx12eu",
          "name": "name",
          "type": "text",
          "required": true,
          "unique": false,
          "options": {
            "min": null,
            "max": null,
            "pattern": ""
          }
        },
        {
          "system": false,
          "id": "flunqi9k",
          "name": "owner",
          "type": "relation",
          "required": false,
          "unique": false,
          "options": {
            "collectionId": "_pb_users_auth_",
            "cascadeDelete": false,
            "minSelect": null,
            "maxSelect": 1,
            "displayFields": []
          }
        },
        {
          "system": false,
          "id": "or8ql4jj",
          "name": "description",
          "type": "text",
          "required": false,
          "unique": false,
          "options": {
            "min": null,
            "max": null,
            "pattern": ""
          }
        }
      ],
      "indexes": [
        "CREATE UNIQUE INDEX `idx_RpTwAg7` ON `workspaces` (\n  `name`,\n  `owner`\n)"
      ],
      "listRule": "@request.auth.id = owner.id",
      "viewRule": "@request.auth.id = owner.id",
      "createRule": "@request.auth.id = owner.id",
      "updateRule": null,
      "deleteRule": "@request.auth.id = owner.id",
      "options": {}
    }
  ];

  const collections = snapshot.map((item) => new Collection(item));

  return Dao(db).importCollections(collections, true, null);
}, (db) => {
  return null;
})
