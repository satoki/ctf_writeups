"use strict";
(() => {
  // node_modules/@trpc/server/dist/observable/observable.mjs
  function observable(subscribe) {
    const self = {
      subscribe(observer) {
        let teardownRef = null;
        let isDone = false;
        let unsubscribed = false;
        let teardownImmediately = false;
        function unsubscribe() {
          if (teardownRef === null) {
            teardownImmediately = true;
            return;
          }
          if (unsubscribed) {
            return;
          }
          unsubscribed = true;
          if (typeof teardownRef === "function") {
            teardownRef();
          } else if (teardownRef) {
            teardownRef.unsubscribe();
          }
        }
        teardownRef = subscribe({
          next(value) {
            if (isDone) {
              return;
            }
            observer.next?.(value);
          },
          error(err) {
            if (isDone) {
              return;
            }
            isDone = true;
            observer.error?.(err);
            unsubscribe();
          },
          complete() {
            if (isDone) {
              return;
            }
            isDone = true;
            observer.complete?.();
            unsubscribe();
          }
        });
        if (teardownImmediately) {
          unsubscribe();
        }
        return {
          unsubscribe
        };
      },
      pipe(...operations) {
        return operations.reduce(pipeReducer, self);
      }
    };
    return self;
  }
  function pipeReducer(prev, fn) {
    return fn(prev);
  }
  var ObservableAbortError = class _ObservableAbortError extends Error {
    constructor(message) {
      super(message);
      this.name = "ObservableAbortError";
      Object.setPrototypeOf(this, _ObservableAbortError.prototype);
    }
  };
  function observableToPromise(observable2) {
    let abort;
    const promise = new Promise((resolve, reject) => {
      let isDone = false;
      function onDone() {
        if (isDone) {
          return;
        }
        isDone = true;
        reject(new ObservableAbortError("This operation was aborted."));
        obs$.unsubscribe();
      }
      const obs$ = observable2.subscribe({
        next(data) {
          isDone = true;
          resolve(data);
          onDone();
        },
        error(data) {
          isDone = true;
          reject(data);
          onDone();
        },
        complete() {
          isDone = true;
          onDone();
        }
      });
      abort = onDone;
    });
    return {
      promise,
      // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
      abort
    };
  }

  // node_modules/@trpc/server/dist/observable/operators.mjs
  function share(_opts) {
    return (source) => {
      let refCount = 0;
      let subscription = null;
      const observers = [];
      function startIfNeeded() {
        if (subscription) {
          return;
        }
        subscription = source.subscribe({
          next(value) {
            for (const observer of observers) {
              observer.next?.(value);
            }
          },
          error(error) {
            for (const observer of observers) {
              observer.error?.(error);
            }
          },
          complete() {
            for (const observer of observers) {
              observer.complete?.();
            }
          }
        });
      }
      function resetIfNeeded() {
        if (refCount === 0 && subscription) {
          const _sub = subscription;
          subscription = null;
          _sub.unsubscribe();
        }
      }
      return observable((subscriber) => {
        refCount++;
        observers.push(subscriber);
        startIfNeeded();
        return {
          unsubscribe() {
            refCount--;
            resetIfNeeded();
            const index = observers.findIndex((v) => v === subscriber);
            if (index > -1) {
              observers.splice(index, 1);
            }
          }
        };
      });
    };
  }

  // node_modules/@trpc/client/dist/links/internals/createChain.mjs
  function createChain(opts) {
    return observable((observer) => {
      function execute(index = 0, op = opts.op) {
        const next = opts.links[index];
        if (!next) {
          throw new Error("No more links to execute - did you forget to add an ending link?");
        }
        const subscription = next({
          op,
          next(nextOp) {
            const nextObserver = execute(index + 1, nextOp);
            return nextObserver;
          }
        });
        return subscription;
      }
      const obs$ = execute();
      return obs$.subscribe(observer);
    });
  }

  // node_modules/@trpc/server/dist/unstable-core-do-not-import/createProxy.mjs
  var noop = () => {
  };
  function createInnerProxy(callback, path) {
    const proxy = new Proxy(noop, {
      get(_obj, key) {
        if (typeof key !== "string" || key === "then") {
          return void 0;
        }
        return createInnerProxy(callback, [
          ...path,
          key
        ]);
      },
      apply(_1, _2, args) {
        const lastOfPath = path[path.length - 1];
        let opts = {
          args,
          path
        };
        if (lastOfPath === "call") {
          opts = {
            args: args.length >= 2 ? [
              args[1]
            ] : [],
            path: path.slice(0, -1)
          };
        } else if (lastOfPath === "apply") {
          opts = {
            args: args.length >= 2 ? args[1] : [],
            path: path.slice(0, -1)
          };
        }
        return callback(opts);
      }
    });
    return proxy;
  }
  var createRecursiveProxy = (callback) => createInnerProxy(callback, []);
  var createFlatProxy = (callback) => {
    return new Proxy(noop, {
      get(_obj, name) {
        if (typeof name !== "string" || name === "then") {
          return void 0;
        }
        return callback(name);
      }
    });
  };

  // node_modules/@trpc/server/dist/unstable-core-do-not-import/utils.mjs
  var unsetMarker = Symbol("unsetMarker");
  function mergeWithoutOverrides(obj1, ...objs) {
    const newObj = Object.assign(/* @__PURE__ */ Object.create(null), obj1);
    for (const overrides of objs) {
      for (const key in overrides) {
        if (key in newObj && newObj[key] !== overrides[key]) {
          throw new Error(`Duplicate key ${key}`);
        }
        newObj[key] = overrides[key];
      }
    }
    return newObj;
  }
  function isObject(value) {
    return !!value && !Array.isArray(value) && typeof value === "object";
  }
  function isFunction(fn) {
    return typeof fn === "function";
  }
  function omitPrototype(obj) {
    return Object.assign(/* @__PURE__ */ Object.create(null), obj);
  }

  // node_modules/@trpc/server/dist/unstable-core-do-not-import/error/TRPCError.mjs
  var UnknownCauseError = class extends Error {
  };
  function getCauseFromUnknown(cause) {
    if (cause instanceof Error) {
      return cause;
    }
    const type = typeof cause;
    if (type === "undefined" || type === "function" || cause === null) {
      return void 0;
    }
    if (type !== "object") {
      return new Error(String(cause));
    }
    if (isObject(cause)) {
      const err = new UnknownCauseError();
      for (const key in cause) {
        err[key] = cause[key];
      }
      return err;
    }
    return void 0;
  }
  function getTRPCErrorFromUnknown(cause) {
    if (cause instanceof TRPCError) {
      return cause;
    }
    if (cause instanceof Error && cause.name === "TRPCError") {
      return cause;
    }
    const trpcError = new TRPCError({
      code: "INTERNAL_SERVER_ERROR",
      cause
    });
    if (cause instanceof Error && cause.stack) {
      trpcError.stack = cause.stack;
    }
    return trpcError;
  }
  var TRPCError = class extends Error {
    constructor(opts) {
      const cause = getCauseFromUnknown(opts.cause);
      const message = opts.message ?? cause?.message ?? opts.code;
      super(message, {
        cause
      });
      this.code = opts.code;
      this.name = "TRPCError";
      if (!this.cause) {
        this.cause = cause;
      }
    }
  };

  // node_modules/@trpc/server/dist/unstable-core-do-not-import/error/formatter.mjs
  var defaultFormatter = ({ shape }) => {
    return shape;
  };

  // node_modules/@trpc/server/dist/unstable-core-do-not-import/transformer.mjs
  function getDataTransformer(transformer) {
    if ("input" in transformer) {
      return transformer;
    }
    return {
      input: transformer,
      output: transformer
    };
  }
  var defaultTransformer = {
    input: {
      serialize: (obj) => obj,
      deserialize: (obj) => obj
    },
    output: {
      serialize: (obj) => obj,
      deserialize: (obj) => obj
    }
  };
  function transformResultInner(response, transformer) {
    if ("error" in response) {
      const error = transformer.deserialize(response.error);
      return {
        ok: false,
        error: {
          ...response,
          error
        }
      };
    }
    const result = {
      ...response.result,
      ...(!response.result.type || response.result.type === "data") && {
        type: "data",
        data: transformer.deserialize(response.result.data)
      }
    };
    return {
      ok: true,
      result
    };
  }
  var TransformResultError = class extends Error {
    constructor() {
      super("Unable to transform response from server");
    }
  };
  function transformResult(response, transformer) {
    let result;
    try {
      result = transformResultInner(response, transformer);
    } catch (err) {
      throw new TransformResultError();
    }
    if (!result.ok && (!isObject(result.error.error) || typeof result.error.error["code"] !== "number")) {
      throw new TransformResultError();
    }
    if (result.ok && !isObject(result.result)) {
      throw new TransformResultError();
    }
    return result;
  }

  // node_modules/@trpc/server/dist/unstable-core-do-not-import/router.mjs
  function isRouter(procedureOrRouter) {
    return procedureOrRouter._def && "router" in procedureOrRouter._def;
  }
  var emptyRouter = {
    _ctx: null,
    _errorShape: null,
    _meta: null,
    queries: {},
    mutations: {},
    subscriptions: {},
    errorFormatter: defaultFormatter,
    transformer: defaultTransformer
  };
  var reservedWords = [
    /**
    * Then is a reserved word because otherwise we can't return a promise that returns a Proxy
    * since JS will think that `.then` is something that exists
    */
    "then",
    /**
    * `fn.call()` and `fn.apply()` are reserved words because otherwise we can't call a function using `.call` or `.apply`
    */
    "call",
    "apply"
  ];
  function createRouterFactory(config) {
    function createRouterInner(input) {
      const reservedWordsUsed = new Set(Object.keys(input).filter((v) => reservedWords.includes(v)));
      if (reservedWordsUsed.size > 0) {
        throw new Error("Reserved words used in `router({})` call: " + Array.from(reservedWordsUsed).join(", "));
      }
      const procedures = omitPrototype({});
      function step(from, path = []) {
        const aggregate = omitPrototype({});
        for (const [key, item] of Object.entries(from ?? {})) {
          if (isRouter(item)) {
            aggregate[key] = step(item._def.record, [
              ...path,
              key
            ]);
            continue;
          }
          if (!isProcedure(item)) {
            aggregate[key] = step(item, [
              ...path,
              key
            ]);
            continue;
          }
          const newPath = [
            ...path,
            key
          ].join(".");
          if (procedures[newPath]) {
            throw new Error(`Duplicate key: ${newPath}`);
          }
          procedures[newPath] = item;
          aggregate[key] = item;
        }
        return aggregate;
      }
      const record = step(input);
      const _def = {
        _config: config,
        router: true,
        procedures,
        ...emptyRouter,
        record
      };
      return {
        ...record,
        _def,
        createCaller: createCallerFactory()({
          _def
        })
      };
    }
    return createRouterInner;
  }
  function isProcedure(procedureOrRouter) {
    return typeof procedureOrRouter === "function";
  }
  function createCallerFactory() {
    return function createCallerInner(router) {
      const _def = router._def;
      return function createCaller(ctxOrCallback, options) {
        const proxy = createRecursiveProxy(async ({ path, args }) => {
          const fullPath = path.join(".");
          const procedure = _def.procedures[fullPath];
          let ctx = void 0;
          try {
            ctx = isFunction(ctxOrCallback) ? await Promise.resolve(ctxOrCallback()) : ctxOrCallback;
            return await procedure({
              path: fullPath,
              getRawInput: async () => args[0],
              ctx,
              type: procedure._def.type
            });
          } catch (cause) {
            options?.onError?.({
              ctx,
              error: getTRPCErrorFromUnknown(cause),
              input: args[0],
              path: fullPath,
              type: procedure._def.type
            });
            throw cause;
          }
        });
        return proxy;
      };
    };
  }
  function mergeRouters(...routerList) {
    const record = mergeWithoutOverrides({}, ...routerList.map((r) => r._def.record));
    const errorFormatter = routerList.reduce((currentErrorFormatter, nextRouter) => {
      if (nextRouter._def._config.errorFormatter && nextRouter._def._config.errorFormatter !== defaultFormatter) {
        if (currentErrorFormatter !== defaultFormatter && currentErrorFormatter !== nextRouter._def._config.errorFormatter) {
          throw new Error("You seem to have several error formatters");
        }
        return nextRouter._def._config.errorFormatter;
      }
      return currentErrorFormatter;
    }, defaultFormatter);
    const transformer = routerList.reduce((prev, current) => {
      if (current._def._config.transformer && current._def._config.transformer !== defaultTransformer) {
        if (prev !== defaultTransformer && prev !== current._def._config.transformer) {
          throw new Error("You seem to have several transformers");
        }
        return current._def._config.transformer;
      }
      return prev;
    }, defaultTransformer);
    const router = createRouterFactory({
      errorFormatter,
      transformer,
      isDev: routerList.every((r) => r._def._config.isDev),
      allowOutsideOfServer: routerList.every((r) => r._def._config.allowOutsideOfServer),
      isServer: routerList.every((r) => r._def._config.isServer),
      $types: routerList[0]?._def._config.$types
    })(record);
    return router;
  }

  // node_modules/@trpc/server/dist/unstable-core-do-not-import/middleware.mjs
  var middlewareMarker = "middlewareMarker";
  function createMiddlewareFactory() {
    function createMiddlewareInner(middlewares) {
      return {
        _middlewares: middlewares,
        unstable_pipe(middlewareBuilderOrFn) {
          const pipedMiddleware = "_middlewares" in middlewareBuilderOrFn ? middlewareBuilderOrFn._middlewares : [
            middlewareBuilderOrFn
          ];
          return createMiddlewareInner([
            ...middlewares,
            ...pipedMiddleware
          ]);
        }
      };
    }
    function createMiddleware(fn) {
      return createMiddlewareInner([
        fn
      ]);
    }
    return createMiddleware;
  }
  function createInputMiddleware(parse) {
    const inputMiddleware = async function inputValidatorMiddleware(opts) {
      let parsedInput;
      const rawInput = await opts.getRawInput();
      try {
        parsedInput = await parse(rawInput);
      } catch (cause) {
        throw new TRPCError({
          code: "BAD_REQUEST",
          cause
        });
      }
      const combinedInput = isObject(opts.input) && isObject(parsedInput) ? {
        ...opts.input,
        ...parsedInput
      } : parsedInput;
      return opts.next({
        input: combinedInput
      });
    };
    inputMiddleware._type = "input";
    return inputMiddleware;
  }
  function createOutputMiddleware(parse) {
    const outputMiddleware = async function outputValidatorMiddleware({ next }) {
      const result = await next();
      if (!result.ok) {
        return result;
      }
      try {
        const data = await parse(result.data);
        return {
          ...result,
          data
        };
      } catch (cause) {
        throw new TRPCError({
          message: "Output validation failed",
          code: "INTERNAL_SERVER_ERROR",
          cause
        });
      }
    };
    outputMiddleware._type = "output";
    return outputMiddleware;
  }

  // node_modules/@trpc/server/dist/unstable-core-do-not-import/parser.mjs
  function getParseFn(procedureParser) {
    const parser = procedureParser;
    if (typeof parser === "function") {
      return parser;
    }
    if (typeof parser.parseAsync === "function") {
      return parser.parseAsync.bind(parser);
    }
    if (typeof parser.parse === "function") {
      return parser.parse.bind(parser);
    }
    if (typeof parser.validateSync === "function") {
      return parser.validateSync.bind(parser);
    }
    if (typeof parser.create === "function") {
      return parser.create.bind(parser);
    }
    if (typeof parser.assert === "function") {
      return (value) => {
        parser.assert(value);
        return value;
      };
    }
    throw new Error("Could not find a validator fn");
  }

  // node_modules/@trpc/server/dist/unstable-core-do-not-import/procedureBuilder.mjs
  function createNewBuilder(def1, def2) {
    const { middlewares = [], inputs, meta, ...rest } = def2;
    return createBuilder({
      ...mergeWithoutOverrides(def1, rest),
      inputs: [
        ...def1.inputs,
        ...inputs ?? []
      ],
      middlewares: [
        ...def1.middlewares,
        ...middlewares
      ],
      meta: def1.meta && meta ? {
        ...def1.meta,
        ...meta
      } : meta ?? def1.meta
    });
  }
  function createBuilder(initDef = {}) {
    const _def = {
      procedure: true,
      inputs: [],
      middlewares: [],
      ...initDef
    };
    const builder = {
      _def,
      input(input) {
        const parser = getParseFn(input);
        return createNewBuilder(_def, {
          inputs: [
            input
          ],
          middlewares: [
            createInputMiddleware(parser)
          ]
        });
      },
      output(output) {
        const parser = getParseFn(output);
        return createNewBuilder(_def, {
          output,
          middlewares: [
            createOutputMiddleware(parser)
          ]
        });
      },
      meta(meta) {
        return createNewBuilder(_def, {
          meta
        });
      },
      use(middlewareBuilderOrFn) {
        const middlewares = "_middlewares" in middlewareBuilderOrFn ? middlewareBuilderOrFn._middlewares : [
          middlewareBuilderOrFn
        ];
        return createNewBuilder(_def, {
          middlewares
        });
      },
      unstable_concat(builder2) {
        return createNewBuilder(_def, builder2._def);
      },
      query(resolver) {
        return createResolver({
          ..._def,
          type: "query"
        }, resolver);
      },
      mutation(resolver) {
        return createResolver({
          ..._def,
          type: "mutation"
        }, resolver);
      },
      subscription(resolver) {
        return createResolver({
          ..._def,
          type: "subscription"
        }, resolver);
      },
      experimental_caller(caller) {
        return createNewBuilder(_def, {
          caller
        });
      }
    };
    return builder;
  }
  function createResolver(_defIn, resolver) {
    const finalBuilder = createNewBuilder(_defIn, {
      resolver,
      middlewares: [
        async function resolveMiddleware(opts) {
          const data = await resolver(opts);
          return {
            marker: middlewareMarker,
            ok: true,
            data,
            ctx: opts.ctx
          };
        }
      ]
    });
    const _def = {
      ...finalBuilder._def,
      type: _defIn.type,
      experimental_caller: Boolean(finalBuilder._def.caller),
      meta: finalBuilder._def.meta,
      $types: null
    };
    const invoke = createProcedureCaller(finalBuilder._def);
    const callerOverride = finalBuilder._def.caller;
    if (!callerOverride) {
      return invoke;
    }
    const callerWrapper = async (...args) => {
      return await callerOverride({
        args,
        invoke,
        _def
      });
    };
    callerWrapper._def = _def;
    return callerWrapper;
  }
  var codeblock = `
This is a client-only function.
If you want to call this function on the server, see https://trpc.io/docs/v11/server/server-side-calls
`.trim();
  function createProcedureCaller(_def) {
    async function procedure(opts) {
      if (!opts || !("getRawInput" in opts)) {
        throw new Error(codeblock);
      }
      async function callRecursive(callOpts = {
        index: 0,
        ctx: opts.ctx
      }) {
        try {
          const middleware = _def.middlewares[callOpts.index];
          const result2 = await middleware({
            ctx: callOpts.ctx,
            type: opts.type,
            path: opts.path,
            getRawInput: callOpts.getRawInput ?? opts.getRawInput,
            meta: _def.meta,
            input: callOpts.input,
            next(_nextOpts) {
              const nextOpts = _nextOpts;
              return callRecursive({
                index: callOpts.index + 1,
                ctx: nextOpts && "ctx" in nextOpts ? {
                  ...callOpts.ctx,
                  ...nextOpts.ctx
                } : callOpts.ctx,
                input: nextOpts && "input" in nextOpts ? nextOpts.input : callOpts.input,
                getRawInput: nextOpts && "getRawInput" in nextOpts ? nextOpts.getRawInput : callOpts.getRawInput
              });
            }
          });
          return result2;
        } catch (cause) {
          return {
            ok: false,
            error: getTRPCErrorFromUnknown(cause),
            marker: middlewareMarker
          };
        }
      }
      const result = await callRecursive();
      if (!result) {
        throw new TRPCError({
          code: "INTERNAL_SERVER_ERROR",
          message: "No result from middlewares - did you forget to `return next()`?"
        });
      }
      if (!result.ok) {
        throw result.error;
      }
      return result.data;
    }
    procedure._def = _def;
    return procedure;
  }

  // node_modules/@trpc/server/dist/unstable-core-do-not-import/rootConfig.mjs
  var isServerDefault = typeof window === "undefined" || "Deno" in window || // eslint-disable-next-line @typescript-eslint/dot-notation
  globalThis.process?.env?.["NODE_ENV"] === "test" || !!globalThis.process?.env?.["JEST_WORKER_ID"] || !!globalThis.process?.env?.["VITEST_WORKER_ID"];

  // node_modules/@trpc/server/dist/unstable-core-do-not-import/initTRPC.mjs
  var TRPCBuilder = class _TRPCBuilder {
    /**
    * Add a context shape as a generic to the root object
    * @link https://trpc.io/docs/v11/server/context
    */
    context() {
      return new _TRPCBuilder();
    }
    /**
    * Add a meta shape as a generic to the root object
    * @link https://trpc.io/docs/v11/quickstart
    */
    meta() {
      return new _TRPCBuilder();
    }
    /**
    * Create the root object
    * @link https://trpc.io/docs/v11/server/routers#initialize-trpc
    */
    create(opts) {
      const config = {
        transformer: getDataTransformer(opts?.transformer ?? defaultTransformer),
        isDev: opts?.isDev ?? // eslint-disable-next-line @typescript-eslint/dot-notation
        globalThis.process?.env["NODE_ENV"] !== "production",
        allowOutsideOfServer: opts?.allowOutsideOfServer ?? false,
        errorFormatter: opts?.errorFormatter ?? defaultFormatter,
        isServer: opts?.isServer ?? isServerDefault,
        /**
        * These are just types, they can't be used at runtime
        * @internal
        */
        $types: null,
        experimental: opts?.experimental ?? {}
      };
      {
        const isServer = opts?.isServer ?? isServerDefault;
        if (!isServer && opts?.allowOutsideOfServer !== true) {
          throw new Error(`You're trying to use @trpc/server in a non-server environment. This is not supported by default.`);
        }
      }
      return {
        /**
        * Your router config
        * @internal
        */
        _config: config,
        /**
        * Builder object for creating procedures
        * @link https://trpc.io/docs/v11/server/procedures
        */
        procedure: createBuilder({
          meta: opts?.defaultMeta
        }),
        /**
        * Create reusable middlewares
        * @link https://trpc.io/docs/v11/server/middlewares
        */
        middleware: createMiddlewareFactory(),
        /**
        * Create a router
        * @link https://trpc.io/docs/v11/server/routers
        */
        router: createRouterFactory(config),
        /**
        * Merge Routers
        * @link https://trpc.io/docs/v11/server/merging-routers
        */
        mergeRouters,
        /**
        * Create a server-side caller for a router
        * @link https://trpc.io/docs/v11/server/server-side-calls
        */
        createCallerFactory: createCallerFactory()
      };
    }
  };
  var initTRPC = new TRPCBuilder();

  // node_modules/@trpc/server/dist/unstable-core-do-not-import/types.mjs
  var ERROR_SYMBOL = Symbol("TypeError");

  // node_modules/@trpc/client/dist/TRPCClientError.mjs
  function isTRPCClientError(cause) {
    return cause instanceof TRPCClientError || /**
    * @deprecated
    * Delete in next major
    */
    cause instanceof Error && cause.name === "TRPCClientError";
  }
  function isTRPCErrorResponse(obj) {
    return isObject(obj) && isObject(obj["error"]) && typeof obj["error"]["code"] === "number" && typeof obj["error"]["message"] === "string";
  }
  var TRPCClientError = class _TRPCClientError extends Error {
    static from(_cause, opts = {}) {
      const cause = _cause;
      if (isTRPCClientError(cause)) {
        if (opts.meta) {
          cause.meta = {
            ...cause.meta,
            ...opts.meta
          };
        }
        return cause;
      }
      if (isTRPCErrorResponse(cause)) {
        return new _TRPCClientError(cause.error.message, {
          ...opts,
          result: cause
        });
      }
      if (!(cause instanceof Error)) {
        return new _TRPCClientError("Unknown error", {
          ...opts,
          cause
        });
      }
      return new _TRPCClientError(cause.message, {
        ...opts,
        cause: getCauseFromUnknown(cause)
      });
    }
    constructor(message, opts) {
      const cause = opts?.cause;
      super(message, {
        cause
      });
      this.meta = opts?.meta;
      this.cause = cause;
      this.shape = opts?.result?.error;
      this.data = opts?.result?.error.data;
      this.name = "TRPCClientError";
      Object.setPrototypeOf(this, _TRPCClientError.prototype);
    }
  };

  // node_modules/@trpc/client/dist/internals/TRPCUntypedClient.mjs
  var TRPCUntypedClient = class {
    $request({ type, input, path, context = {} }) {
      const chain$ = createChain({
        links: this.links,
        op: {
          id: ++this.requestId,
          type,
          path,
          input,
          context
        }
      });
      return chain$.pipe(share());
    }
    requestAsPromise(opts) {
      const req$ = this.$request(opts);
      const { promise, abort } = observableToPromise(req$);
      const abortablePromise = new Promise((resolve, reject) => {
        opts.signal?.addEventListener("abort", abort);
        promise.then((envelope) => {
          resolve(envelope.result.data);
        }).catch((err) => {
          reject(TRPCClientError.from(err));
        });
      });
      return abortablePromise;
    }
    query(path, input, opts) {
      return this.requestAsPromise({
        type: "query",
        path,
        input,
        context: opts?.context,
        signal: opts?.signal
      });
    }
    mutation(path, input, opts) {
      return this.requestAsPromise({
        type: "mutation",
        path,
        input,
        context: opts?.context,
        signal: opts?.signal
      });
    }
    subscription(path, input, opts) {
      const observable$ = this.$request({
        type: "subscription",
        path,
        input,
        context: opts?.context
      });
      return observable$.subscribe({
        next(envelope) {
          if (envelope.result.type === "started") {
            opts.onStarted?.();
          } else if (envelope.result.type === "stopped") {
            opts.onStopped?.();
          } else {
            opts.onData?.(envelope.result.data);
          }
        },
        error(err) {
          opts.onError?.(err);
        },
        complete() {
          opts.onComplete?.();
        }
      });
    }
    constructor(opts) {
      this.requestId = 0;
      this.runtime = {};
      this.links = opts.links.map((link) => link(this.runtime));
    }
  };

  // node_modules/@trpc/client/dist/createTRPCClient.mjs
  var clientCallTypeMap = {
    query: "query",
    mutate: "mutation",
    subscribe: "subscription"
  };
  var clientCallTypeToProcedureType = (clientCallType) => {
    return clientCallTypeMap[clientCallType];
  };
  function createTRPCClientProxy(client2) {
    return createFlatProxy((key) => {
      if (client2.hasOwnProperty(key)) {
        return client2[key];
      }
      if (key === "__untypedClient") {
        return client2;
      }
      return createRecursiveProxy(({ path, args }) => {
        const pathCopy = [
          key,
          ...path
        ];
        const procedureType = clientCallTypeToProcedureType(pathCopy.pop());
        const fullPath = pathCopy.join(".");
        return client2[procedureType](fullPath, ...args);
      });
    });
  }
  function createTRPCClient(opts) {
    const client2 = new TRPCUntypedClient(opts);
    const proxy = createTRPCClientProxy(client2);
    return proxy;
  }

  // node_modules/@trpc/client/dist/getFetch.mjs
  var isFunction2 = (fn) => typeof fn === "function";
  function getFetch(customFetchImpl) {
    if (customFetchImpl) {
      return customFetchImpl;
    }
    if (typeof window !== "undefined" && isFunction2(window.fetch)) {
      return window.fetch;
    }
    if (typeof globalThis !== "undefined" && isFunction2(globalThis.fetch)) {
      return globalThis.fetch;
    }
    throw new Error("No fetch implementation found");
  }

  // node_modules/@trpc/client/dist/links/internals/contentTypes.mjs
  function isOctetType(input) {
    return input instanceof Uint8Array || // File extends from Blob but is only available in nodejs from v20
    input instanceof Blob;
  }
  function isFormData(input) {
    return input instanceof FormData;
  }

  // node_modules/@trpc/client/dist/internals/getAbortController.mjs
  function getAbortController(customAbortControllerImpl) {
    if (customAbortControllerImpl) {
      return customAbortControllerImpl;
    }
    if (typeof window !== "undefined" && window.AbortController) {
      return window.AbortController;
    }
    if (typeof globalThis !== "undefined" && globalThis.AbortController) {
      return globalThis.AbortController;
    }
    return null;
  }

  // node_modules/@trpc/client/dist/internals/transformer.mjs
  function getTransformer(transformer) {
    const _transformer = transformer;
    if (!_transformer) {
      return {
        input: {
          serialize: (data) => data,
          deserialize: (data) => data
        },
        output: {
          serialize: (data) => data,
          deserialize: (data) => data
        }
      };
    }
    if ("input" in _transformer) {
      return _transformer;
    }
    return {
      input: _transformer,
      output: _transformer
    };
  }

  // node_modules/@trpc/client/dist/links/internals/httpUtils.mjs
  function resolveHTTPLinkOptions(opts) {
    return {
      url: opts.url.toString().replace(/\/$/, ""),
      fetch: opts.fetch,
      AbortController: getAbortController(opts.AbortController),
      transformer: getTransformer(opts.transformer),
      methodOverride: opts.methodOverride
    };
  }
  function arrayToDict(array) {
    const dict = {};
    for (let index = 0; index < array.length; index++) {
      const element = array[index];
      dict[index] = element;
    }
    return dict;
  }
  var METHOD = {
    query: "GET",
    mutation: "POST"
  };
  function getInput(opts) {
    return "input" in opts ? opts.transformer.input.serialize(opts.input) : arrayToDict(opts.inputs.map((_input) => opts.transformer.input.serialize(_input)));
  }
  var getUrl = (opts) => {
    let url = opts.url + "/" + opts.path;
    const queryParts = [];
    if ("inputs" in opts) {
      queryParts.push("batch=1");
    }
    if (opts.type === "query") {
      const input = getInput(opts);
      if (input !== void 0 && opts.methodOverride !== "POST") {
        queryParts.push(`input=${encodeURIComponent(JSON.stringify(input))}`);
      }
    }
    if (queryParts.length) {
      url += "?" + queryParts.join("&");
    }
    return url;
  };
  var getBody = (opts) => {
    if (opts.type === "query" && opts.methodOverride !== "POST") {
      return void 0;
    }
    const input = getInput(opts);
    return input !== void 0 ? JSON.stringify(input) : void 0;
  };
  var jsonHttpRequester = (opts) => {
    return httpRequest({
      ...opts,
      contentTypeHeader: "application/json",
      getUrl,
      getBody
    });
  };
  async function fetchHTTPResponse(opts, ac) {
    const url = opts.getUrl(opts);
    const body = opts.getBody(opts);
    const { type } = opts;
    const resolvedHeaders = await (async () => {
      const heads = await opts.headers();
      if (Symbol.iterator in heads) {
        return Object.fromEntries(heads);
      }
      return heads;
    })();
    if (type === "subscription") {
      throw new Error("Subscriptions should use wsLink");
    }
    const headers = {
      ...opts.contentTypeHeader ? {
        "content-type": opts.contentTypeHeader
      } : {},
      ...opts.trpcAcceptHeader ? {
        "trpc-accept": opts.trpcAcceptHeader
      } : void 0,
      ...resolvedHeaders
    };
    return getFetch(opts.fetch)(url, {
      method: opts.methodOverride ?? METHOD[type],
      signal: ac?.signal,
      body,
      headers
    });
  }
  function httpRequest(opts) {
    const ac = opts.AbortController ? new opts.AbortController() : null;
    const meta = {};
    let done = false;
    const promise = new Promise((resolve, reject) => {
      fetchHTTPResponse(opts, ac).then((_res) => {
        meta.response = _res;
        done = true;
        return _res.json();
      }).then((json) => {
        meta.responseJSON = json;
        resolve({
          json,
          meta
        });
      }).catch((err) => {
        done = true;
        reject(TRPCClientError.from(err, {
          meta
        }));
      });
    });
    const cancel = () => {
      if (!done) {
        ac?.abort();
      }
    };
    return {
      promise,
      cancel
    };
  }

  // node_modules/@trpc/client/dist/links/httpLink.mjs
  var universalRequester = (opts) => {
    const input = getInput(opts);
    if (isFormData(input)) {
      if (opts.type !== "mutation" && opts.methodOverride !== "POST") {
        throw new Error("FormData is only supported for mutations");
      }
      return httpRequest({
        ...opts,
        // The browser will set this automatically and include the boundary= in it
        contentTypeHeader: void 0,
        getUrl,
        getBody: () => input
      });
    }
    if (isOctetType(input)) {
      if (opts.type !== "mutation" && opts.methodOverride !== "POST") {
        throw new Error("Octet type input is only supported for mutations");
      }
      return httpRequest({
        ...opts,
        contentTypeHeader: "application/octet-stream",
        getUrl,
        getBody: () => input
      });
    }
    return jsonHttpRequester(opts);
  };
  function httpLink(opts) {
    const resolvedOpts = resolveHTTPLinkOptions(opts);
    return () => {
      return ({ op }) => {
        return observable((observer) => {
          const { path, input, type } = op;
          const request = universalRequester({
            ...resolvedOpts,
            type,
            path,
            input,
            headers() {
              if (!opts.headers) {
                return {};
              }
              if (typeof opts.headers === "function") {
                return opts.headers({
                  op
                });
              }
              return opts.headers;
            }
          });
          let meta = void 0;
          request.promise.then((res) => {
            meta = res.meta;
            const transformed = transformResult(res.json, resolvedOpts.transformer.output);
            if (!transformed.ok) {
              observer.error(TRPCClientError.from(transformed.error, {
                meta
              }));
              return;
            }
            observer.next({
              context: res.meta,
              result: transformed.result
            });
            observer.complete();
          }).catch((cause) => {
            observer.error(TRPCClientError.from(cause, {
              meta
            }));
          });
          return () => {
            request.cancel();
          };
        });
      };
    };
  }

  // client.ts
  var client = createTRPCClient({ links: [
    httpLink({
      url: "/api",
      headers: () => {
        const username = localStorage.getItem("username");
        const password = localStorage.getItem("password");
        return { login: `${username}:${password}` };
      }
    })
  ] });
  var checkLogin = async () => {
    try {
      const result = await client.user.query();
      return result.user;
    } catch {
      return void 0;
    }
  };
  var getPicture = async (username) => {
    const params = new URLSearchParams({ username });
    const result = await fetch(`/picture?${params}`).then((res) => res.text());
    return result || "/default.png";
  };
  var getTickles = async (username) => {
    const result = await client.getTickles.query({ username });
    if (!result.success) {
      return void 0;
    }
    return result.count;
  };
  var routes = {
    "/": async () => {
      const p = document.querySelector("p");
      const login = await checkLogin();
      if (login !== void 0) {
        const link = document.createElement("a");
        link.textContent = login;
        link.href = "/profile";
        const text = document.createTextNode("Logged in as ");
        const period = document.createTextNode(".");
        p.appendChild(text);
        p.appendChild(link);
        p.appendChild(period);
      } else {
        const login2 = document.createElement("a");
        login2.textContent = "sign in";
        login2.href = "/login";
        const register = document.createElement("a");
        register.textContent = "register";
        register.href = "/register";
        p.append(
          document.createTextNode("Not logged in ("),
          login2,
          document.createTextNode(" or "),
          register,
          document.createTextNode(").")
        );
      }
    },
    "/login": async () => {
      const form = document.querySelector("form");
      const error = document.querySelector("p");
      const query = new URLSearchParams(window.location.search);
      if (query.has("error")) {
        error.innerHTML = query.get("error") ?? "";
      }
      form.addEventListener("submit", async (event) => {
        event.preventDefault();
        const username = form.elements.namedItem("n");
        const password = form.elements.namedItem("p");
        const result = await client.doLogin.mutate({
          username: username.value,
          password: password.value
        });
        if (!result.success) {
          error.textContent = `Login failed. ${result.message}`;
        } else {
          localStorage.setItem("username", username.value);
          localStorage.setItem("password", password.value);
          window.location.href = "/";
        }
      });
    },
    "/register": async () => {
      const suggest = document.querySelector("code");
      const copy = document.querySelector("button");
      const password = document.querySelector(
        "input[name=p]"
      );
      const form = document.querySelector("form");
      const random = crypto.randomUUID().replace(/-/g, "");
      suggest.textContent = random;
      copy.addEventListener("click", () => {
        navigator.clipboard.writeText(random);
        password.value = random;
      });
      form.addEventListener("submit", async (event) => {
        event.preventDefault();
        const username = form.elements.namedItem("n");
        const password2 = form.elements.namedItem("p");
        const result = await client.doRegister.mutate({
          username: username.value,
          password: password2.value
        });
        if (!result.success) {
          suggest.textContent = result.message;
        } else {
          localStorage.setItem("username", username.value);
          localStorage.setItem("password", password2.value);
          window.location.href = "/";
        }
      });
    },
    "/profile": async () => {
      const login = await checkLogin();
      if (!login) {
        window.location.href = "/login?error=Not+logged+in.";
        return;
      }
      const picture = document.querySelector("img");
      const text = document.querySelector(".tickles");
      const form = document.querySelector("form");
      const error = document.querySelector(".error");
      picture.src = await getPicture(login);
      text.textContent = `You have been tickled ${await getTickles(login) ?? 0} times.`;
      form.addEventListener("submit", async (event) => {
        event.preventDefault();
        const url = form.elements.namedItem("image");
        const result = await client.setPicture.mutate({ url: url.value });
        if (!result.success) {
          error.textContent = result.message;
        } else {
          const data = await getPicture(login);
          picture.src = data;
        }
      });
    },
    "/user": async () => {
      const query = new URLSearchParams(window.location.search);
      const username = query.get("name");
      const div = document.querySelector(".container");
      const stack = document.querySelector(".stack");
      const picture = document.querySelector("img");
      const name = div.querySelector(".username");
      const count = div.querySelector(".tickles");
      const error = () => div.textContent = "Not found.";
      if (username === null) return error();
      const tickles = await getTickles(username);
      if (tickles === void 0) return error();
      const image = await getPicture(username);
      picture.src = image;
      name.textContent = `User ${username}.`;
      count.textContent = `Tickled ${tickles} times.`;
      const me = await checkLogin();
      if (me !== void 0 && me !== username) {
        const button = document.createElement("button");
        button.textContent = "Tickle!";
        button.addEventListener("click", async () => {
          const result = await client.doTickle.mutate({ username });
          if (result.success) {
            window.location.reload();
          }
        });
        stack.appendChild(button);
      }
    }
  };
  window.addEventListener("load", () => {
    const element = document.querySelector(
      "meta[name=route]"
    );
    const route = element?.content ?? "/";
    routes[route]?.();
  });
})();
/*! Bundled license information:

@trpc/server/dist/unstable-core-do-not-import/rpc/parseTRPCMessage.mjs:
  (* istanbul ignore next -- @preserve *)

@trpc/server/dist/unstable-core-do-not-import/rpc/parseTRPCMessage.mjs:
  (* istanbul ignore next -- @preserve *)

@trpc/server/dist/unstable-core-do-not-import/rpc/parseTRPCMessage.mjs:
  (* istanbul ignore next -- @preserve *)

@trpc/server/dist/unstable-core-do-not-import/rpc/parseTRPCMessage.mjs:
  (* istanbul ignore next -- @preserve *)

@trpc/server/dist/unstable-core-do-not-import/rpc/parseTRPCMessage.mjs:
  (* istanbul ignore next -- @preserve *)

@trpc/client/dist/links/internals/httpUtils.mjs:
  (* istanbul ignore if -- @preserve *)
*/
