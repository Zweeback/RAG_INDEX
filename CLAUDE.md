# CLAUDE.md - AI Assistant Guide for RAG_INDEX

## Project Overview

**RAG_INDEX** is a Retrieval-Augmented Generation (RAG) indexing system. This repository is currently in its initial setup phase and will evolve to support document indexing, vector storage, and retrieval capabilities for AI-powered applications.

## Repository Status

⚠️ **Repository is currently empty** - This is a fresh project ready for initial development.

## Project Purpose

RAG systems combine the power of large language models with external knowledge retrieval. This project aims to provide:

- **Document Indexing**: Efficient ingestion and processing of various document types
- **Vector Storage**: Embedding generation and vector database integration
- **Retrieval Mechanisms**: Fast and accurate similarity search
- **Query Processing**: Intelligent context retrieval for LLM enhancement

## Expected Codebase Structure

As this project develops, the following structure is recommended:

```
RAG_INDEX/
├── src/                          # Source code
│   ├── indexing/                 # Document ingestion and processing
│   ├── embedding/                # Vector embedding generation
│   ├── storage/                  # Vector database interfaces
│   ├── retrieval/                # Search and retrieval logic
│   └── utils/                    # Shared utilities
├── tests/                        # Test suite
│   ├── unit/                     # Unit tests
│   ├── integration/              # Integration tests
│   └── fixtures/                 # Test data
├── docs/                         # Documentation
├── config/                       # Configuration files
├── scripts/                      # Build and deployment scripts
├── examples/                     # Usage examples
├── requirements.txt or package.json  # Dependencies
└── README.md                     # Project documentation
```

## Technology Stack Considerations

### Common RAG Stack Options

1. **Python-based Stack** (Recommended for ML/AI workloads):
   - **Vector Databases**: Pinecone, Weaviate, Qdrant, ChromaDB, FAISS
   - **Embedding Models**: OpenAI, Cohere, Sentence Transformers
   - **Frameworks**: LangChain, LlamaIndex, Haystack
   - **Document Processing**: PyPDF2, python-docx, BeautifulSoup4

2. **TypeScript/Node.js Stack**:
   - **Vector Databases**: Pinecone, Weaviate client libraries
   - **Frameworks**: LangChain.js
   - **Document Processing**: pdf-parse, mammoth, cheerio

3. **Hybrid Approach**:
   - Python for ML/embedding operations
   - Node.js/TypeScript for API and application layer

## Development Workflow

### Git Branch Strategy

- **Main Branch**: Stable, production-ready code
- **Feature Branches**: Named as `feature/<feature-name>` or `claude/<session-id>`
- **Development Branch**: `develop` for integration testing

### Commit Guidelines

- Use clear, descriptive commit messages
- Format: `<type>: <subject>`
  - Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`
- Example: `feat: add ChromaDB vector storage integration`

### Pull Request Process

1. Create feature branch from main/develop
2. Implement changes with tests
3. Ensure all tests pass
4. Update documentation
5. Submit PR with clear description
6. Address review feedback

## Key Conventions for AI Assistants

### Code Quality Standards

1. **Type Safety**:
   - Use type hints (Python) or TypeScript for type safety
   - Validate input/output types

2. **Error Handling**:
   - Implement proper exception handling
   - Provide meaningful error messages
   - Log errors appropriately

3. **Testing**:
   - Write unit tests for all functions
   - Include integration tests for workflows
   - Aim for >80% code coverage
   - Test edge cases and error conditions

4. **Documentation**:
   - Document all public APIs
   - Include docstrings/JSDoc comments
   - Maintain updated README.md
   - Add inline comments for complex logic

5. **Performance**:
   - Profile embedding operations
   - Optimize vector search queries
   - Implement caching where appropriate
   - Monitor memory usage for large documents

### Security Considerations

1. **API Keys**: Never commit API keys or secrets
   - Use environment variables
   - Provide `.env.example` template
   - Add `.env` to `.gitignore`

2. **Input Validation**: Sanitize all user inputs
   - Validate file types and sizes
   - Prevent injection attacks
   - Limit query complexity

3. **Access Control**: Implement authentication if needed
   - Secure API endpoints
   - Rate limiting for public APIs

### RAG-Specific Best Practices

1. **Chunking Strategy**:
   - Implement configurable chunk sizes (default: 512-1024 tokens)
   - Support overlapping chunks for context preservation
   - Respect document structure (paragraphs, sections)

2. **Embedding Quality**:
   - Choose appropriate embedding models for domain
   - Normalize vectors if required by database
   - Batch embedding operations for efficiency

3. **Retrieval Optimization**:
   - Implement hybrid search (vector + keyword)
   - Support metadata filtering
   - Configure top-k results dynamically
   - Consider re-ranking strategies

4. **Index Management**:
   - Implement incremental indexing
   - Support index versioning
   - Provide index rebuild capabilities
   - Monitor index size and performance

## Configuration Management

Expected configuration parameters:

```yaml
# Example config structure
embedding:
  model: "text-embedding-ada-002"
  dimension: 1536
  batch_size: 100

vector_store:
  type: "chromadb"  # or pinecone, weaviate, etc.
  collection_name: "documents"
  distance_metric: "cosine"

chunking:
  chunk_size: 512
  chunk_overlap: 50
  separator: "\n\n"

retrieval:
  top_k: 5
  similarity_threshold: 0.7
  use_reranking: false
```

## Testing Strategy

### Unit Tests
- Test individual components in isolation
- Mock external dependencies (APIs, databases)
- Fast execution (<1s per test)

### Integration Tests
- Test complete workflows (ingest → index → retrieve)
- Use test vector stores
- Clean up test data after runs

### Performance Tests
- Benchmark embedding generation speed
- Test retrieval latency
- Measure memory usage with large datasets

## Common Tasks for AI Assistants

### When Adding New Features

1. **Read existing code** before proposing changes
2. **Follow established patterns** in the codebase
3. **Add tests** alongside implementation
4. **Update documentation** to reflect changes
5. **Consider backward compatibility**

### When Fixing Bugs

1. **Reproduce the issue** first
2. **Write a failing test** that captures the bug
3. **Fix the issue** with minimal changes
4. **Verify the test passes**
5. **Check for similar issues** elsewhere

### When Refactoring

1. **Ensure tests exist** before refactoring
2. **Make small, incremental changes**
3. **Run tests after each change**
4. **Don't change functionality** during refactoring
5. **Document architectural decisions**

## Dependencies Management

### Python Projects
- Use `requirements.txt` or `pyproject.toml`
- Pin major versions, allow minor updates
- Separate dev dependencies
- Regular security audits with `pip-audit`

### Node.js Projects
- Use `package.json` with `package-lock.json`
- Follow semver principles
- Use `npm audit` for security checks

## Performance Considerations

### Embedding Generation
- Batch API calls to reduce latency
- Cache embeddings for repeated queries
- Consider local models for high-volume use

### Vector Search
- Tune index parameters (HNSW, IVF, etc.)
- Use approximate nearest neighbor (ANN) for scale
- Implement connection pooling

### Document Processing
- Stream large files instead of loading into memory
- Parallel processing for multiple documents
- Implement retry logic for failures

## Monitoring and Observability

Implement logging for:
- Document ingestion rate
- Embedding generation latency
- Retrieval query performance
- Error rates and types
- Cache hit/miss ratios

## Environment Setup

### Prerequisites
- Python 3.9+ or Node.js 18+ (based on final stack choice)
- Vector database (local or cloud)
- API keys for embedding providers (if using external services)

### Installation Steps
```bash
# Clone repository
git clone <repository-url>
cd RAG_INDEX

# Install dependencies (Python example)
pip install -r requirements.txt

# Or for Node.js
npm install

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run tests
pytest  # or npm test

# Start development server
python main.py  # or npm run dev
```

## Resources and References

### RAG Resources
- [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks (Paper)](https://arxiv.org/abs/2005.11401)
- [LangChain Documentation](https://docs.langchain.com/)
- [LlamaIndex Documentation](https://docs.llamaindex.ai/)

### Vector Database Documentation
- [Pinecone Docs](https://docs.pinecone.io/)
- [Weaviate Docs](https://weaviate.io/developers/weaviate)
- [ChromaDB Docs](https://docs.trychroma.com/)
- [Qdrant Docs](https://qdrant.tech/documentation/)

### Best Practices
- [Embedding Best Practices](https://platform.openai.com/docs/guides/embeddings)
- [RAG Techniques](https://www.anyscale.com/blog/a-comprehensive-guide-for-building-rag-based-llm-applications)

## Contact and Support

For questions about this project:
- Review existing documentation in `/docs`
- Check issue tracker for known problems
- Create detailed issues for bugs or feature requests

## Version History

- **v0.1.0** (Initial): Repository created, structure defined

---

**Last Updated**: 2025-11-24

**Note for AI Assistants**: This document will evolve as the project develops. Always check for the latest version and update this file when significant architectural or workflow changes are made.
